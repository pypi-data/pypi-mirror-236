"""Core module of kongxin."""
import multiprocessing as mp
import time
from queue import Empty
from typing import Callable, Optional, TypeVar, Union

import psutil
from loguru import logger
from typing_extensions import ParamSpec

from kongxin.backend.base import BaseBackendABC
from kongxin.bank import task_bank
from kongxin.exception import NotFinished, NotSupported, ProcessFinishedWithoutResult
from kongxin.serialization import serialize
from kongxin.types import (
    JobId,
    JobQuest,
    JobQuestExecution,
    JobResult,
    JobResultType,
    JobStatus,
    JobStatusType,
    SerializationMethod,
    SerializationMethodType,
)

_P = ParamSpec("_P")
_T = TypeVar("_T")


class Core:
    """Core of kongxin.

    Note:
        If you are a user of kongxin,
        you probably don't need to use this class directly.
        Just use the api specified in ``kongxin.api``.

    This class is a singleton.
    You can get the singleton instance by calling ``singleton`` method.
    """

    _SINGLETON: Optional["Core"] = None

    @classmethod
    def singleton(cls) -> "Core":
        """Get the singleton instance of Core."""
        if cls._SINGLETON is None:
            cls._SINGLETON = cls()
        return cls._SINGLETON

    def __init__(self, backend: BaseBackendABC = None):
        """Initialize Core.

        Args:
            backend: backend to use. If not specified, use default backend.
        """
        self._backend = backend
        self._serialization_method = SerializationMethod(
            serializer=SerializationMethodType.PICKLE
        )

        self._consuming_job_quest_exec: Optional[JobQuestExecution] = None
        self._last_submitted: Optional[JobQuest] = None
        # Job quests produced by the current consuming job quest execution
        self._consuming_produced_job_quests: list[JobQuest] = []

    @property
    def backend(self):
        """Backend to use.

        If not specified, use default backend.
        """
        if self._backend is None:
            from kongxin.backend import default_backend

            return default_backend
        return self._backend

    @staticmethod
    def _get_job_func_and_arguments(job_quest_exec: JobQuestExecution):
        func = task_bank.get_func(job_quest_exec.job_quest.func_id)
        args = job_quest_exec.job_quest.args
        kwargs = job_quest_exec.job_quest.kwargs
        if not callable(func):
            raise ValueError(f"func:{func.__qualname__} is not callable")
        if not isinstance(args, tuple):
            raise TypeError(f"args should be tuple, got {type(args)}")
        if not isinstance(kwargs, dict):
            raise TypeError(f"kwargs should be dict, got {type(kwargs)}")
        for key in kwargs:
            if not isinstance(key, str):
                raise TypeError(f"kwargs key should be str, got {type(key)}")
        return func, args, kwargs

    @staticmethod
    def _delegate_func_to_proxy(
        func: Callable[_P, _T],
        args: _P.args,
        kwargs: _P.kwargs,
        result_queue: mp.Queue,
        serialization_method: SerializationMethod,
        job_quest_exec: JobQuestExecution,
    ):
        try:
            Core.singleton()._consuming_job_quest_exec = job_quest_exec
            result = func(*args, **kwargs)
            result_type = JobResultType.RETURN
            detail = "Success"
        except NotFinished as e:
            result = e
            result_type = JobResultType.WAIT_SUBJOB
            detail = str(e)
        except Exception as e:
            result = e
            result_type = JobResultType.RAISE
            detail = str(e)

        serialized_result = serialize(result, serialization_method)
        job_result = JobResult(
            result_type=result_type,
            serialized_result=serialized_result,
            serialization_method=serialization_method,
            detail=detail,
        )

        # kill all sub-processes before exit
        def kill_direct_child(p: psutil.Process):
            for child in p.children():
                kill_direct_child(child)
            try:
                # first send SIGTERM
                p.terminate()
                # wait for 1 second
                try:
                    p.wait(1)
                except psutil.TimeoutExpired:
                    # if not exited, send SIGKILL
                    p.kill()
            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess,
            ):
                pass
            except Exception as exc:
                logger.exception(exc)

        for p in psutil.Process().children():
            kill_direct_child(p)

        # put the result to the result queue
        result_queue.put(job_result)

    def _do_job_unprotected(self, job_quest_exec: JobQuestExecution) -> JobResult:
        func, args, kwargs = self._get_job_func_and_arguments(job_quest_exec)

        sleep_time = 0.1
        result_queue = mp.Queue()

        job_result: Optional[JobResult] = None
        p = mp.Process(
            target=self._delegate_func_to_proxy,
            kwargs=dict(
                func=func,
                args=args,
                kwargs=kwargs,
                result_queue=result_queue,
                serialization_method=self._serialization_method,
                job_quest_exec=job_quest_exec,
            ),
        )
        p.start()

        has_result = False
        while p.is_alive():
            try:
                job_result = result_queue.get_nowait()
                has_result = True
                break
            except Empty:
                pass
            time.sleep(sleep_time)

        if not has_result:
            try:
                job_result = result_queue.get_nowait()
            except Empty:
                raise ProcessFinishedWithoutResult(job_quest_exec=job_quest_exec)

        if job_result is None:
            raise ProcessFinishedWithoutResult(job_quest_exec=job_quest_exec)

        return job_result

    def _do_job(self, job_quest_exec: JobQuestExecution) -> JobResult:
        try:
            return self._do_job_unprotected(job_quest_exec)
        except Exception as e:
            if str(e).startswith("Can't pickle"):
                raise e
            return JobResult(
                result_type=JobResultType.ERROR,
                serialized_result=serialize(e, self._serialization_method),
                serialization_method=self._serialization_method,
                detail=str(e),
            )

    def _update_job_status_via_result(
        self, job_quest_exec: JobQuestExecution, job_result: JobResult
    ) -> JobStatus:
        if job_result.result_type == JobResultType.RETURN:
            state = JobStatusType.SUCCESS
            is_finished = True
            is_success = True
        elif job_result.result_type == JobResultType.RAISE:
            state = JobStatusType.FAILED
            is_finished = True
            is_success = False
        elif job_result.result_type == JobResultType.WAIT_SUBJOB:
            is_finished = False
            is_success = False
            state = JobStatusType.WAITING
        else:
            is_finished = True
            is_success = False
            state = JobStatusType.ERROR

        job_status = JobStatus(
            is_finished=is_finished,
            is_success=is_success,
            state=state,
            detail=job_result.detail,
        )

        self.backend.update_job_status(
            job_quest_exec,
            job_status,
        )

        return job_status

    def _try_to_wake_up_parent(self, parent_job_id: JobId) -> bool:
        for child_id in self.backend.get_all_children(parent_job_id):
            if not self._check_job_status(child_id).is_finished:
                return False
        self.backend.set_job_todo(parent_job_id, set_as=True)
        return True

    def consume(self) -> bool:
        """Consume a job quest execution.

        Algorithm:
        1.  Get next job quest execution from backend.
        2.  Execute the job quest execution.
        3.  Save the job result.
        4.  Update the job status.

        The status of the job quest execution will be updated to one of the following:
        1.  SUCCESS: The job quest execution is executed successfully.
        2.  FAILED: The job quest execution is executed unsuccessfully,
                    e.g., raised an exception in user code.
        3.  ERROR: The job quest execution is executed with error,
                    e.g., internet connection error, OOM, etc.
        4.  WAITING: The job quest execution is waiting for sub-jobs.

        Returns:
            True if a job quest execution is consumed.
            False if no job quest execution is consumed.
        """
        # 1. Get next job quest execution from backend.
        job_quest_exec = self.backend.get_next_job_quest()
        if job_quest_exec is None:
            return False
        try:
            # 2. Execute the job quest execution.
            job_result = self._do_job(job_quest_exec)

            # 3. Save the job result.
            self.backend.put_job_result(job_quest_exec, job_result)

            # 4. Update the job status.
            self._update_job_status_via_result(job_quest_exec, job_result)

            # 5. Try to wake up the parent job.
            if job_quest_exec.job_quest.parent_job_id is not None:
                self._try_to_wake_up_parent(job_quest_exec.job_quest.parent_job_id)

        finally:
            self._consuming_produced_job_quests.clear()
        return True

    def _produce(self, job_quest: JobQuest) -> JobId:
        self.backend.add_job(job_quest)
        self._last_submitted = job_quest
        return job_quest.job_id

    def _check_job_status(self, job_id: JobId) -> JobStatus:
        return self.backend.check_job_status(job_id)

    def _get_job_result(self, job_id: JobId) -> JobResult:
        job_status = self._check_job_status(job_id)
        if not job_status.is_finished:
            raise NotFinished(job_status=job_status)
        job_result = self.backend.get_job_result(job_id)
        if job_result is None:
            raise NotFinished(job_status=job_status)
        return job_result

    def submit(self, func: Union[Callable[_P, _T], str]) -> Callable[_P, JobId]:
        """Submit a function as a job.

        When you want to run a time-consuming function, you can submit it as a job.
        The job be a pure function.
        However, kongxin will try to make sure it is executed exactly once.
        There are some situations the job may run more than once:
        1.  Internal issues such as internet connection, job killed, OOM, etc.
        2.  The job called |submit| inside, i.e., a recursive submission.
            For example
            ```
            import kongxin as kx

            def subjob(s):
                return s + 10

            def job():
                sub1 = kx.submit(subjob(1))  # don't worry about submit multiple times
                print('sub1')  # called at most 3 times
                sub2 = kx.submit(subjob(2))  # don't worry about submit multiple times
                print('sub1')  # called at most 3 times
                n1 = kx.get(sub1)
                print('n1')  # called at most 2 times
                n2 = kx.get(sub2)
                print('n2')  # called at most 1 time
                return sum(numbers)

            kx.submit(job)()
            ```
            In the above code, the print can be called multiple times
            based on how many |get| after it.
            However, you don't have to worry about multiple submission,
            kongxin will make sure the subjob is submitted
            exactly once by looking at the callstack.

        When the job executed failed, kongxin will NOT try to re-run it,
        and you will need to catch the exception in your code when you |get| the result.
        For example
        ```
        import kongxin as kx

        def job():
            raise Exception('failed')

        job_id = kx.submit(job)()
        try:
            kx.get(job_id)
        except Exception as e:
            print(e)  # failed
        ```

        Args:
            func (Callable[_P, _T] or str):
                The function to submit.
                If it is a string, it should be the id of the function in the task bank.
                The id to function mapping should be registered in consuming time.

        Returns:
            Callable[P, T]:
                A function that has the same signature as the original function,
                but returns the job id instead of the result.

        Examples:
            >>> import kongxin as kx
            >>> def add(a, b):
            ...     return a + b
            >>> kx.submit(add)(1, 2)
            JobId('...')

        """

        def _submit(*args: _P.args, **kwargs: _P.kwargs) -> JobId:
            if self._consuming_job_quest_exec is None:
                parent_job = None
            else:
                parent_job = self._consuming_job_quest_exec.job_quest
            if callable(func):
                job_quest = task_bank.job_quest(
                    func, parent=parent_job, last_job_quest=self._last_submitted
                )(*args, **kwargs)
            elif isinstance(func, str):
                job_quest = task_bank.job_quest_by_id(
                    func, parent=parent_job, last_job_quest=self._last_submitted
                )(*args, **kwargs)
            else:
                raise NotSupported(f"func should be callable or str, got {type(func)}")

            return self._produce(job_quest)

        return _submit

    def get(self, job_id: JobId):
        """Get the result of a job.

        You can get the result of a job by its job id.
        If the job is not finished, this function will raise ``NotFinished``.
        You can use ``poll`` to check if the job is finished.

        Args:
            job_id: job id

        Returns:
            The return value of the original function
            if the job is finished successfully.

        Raises:
            NotFinished: if the job is not finished.
            WaitSubJobs: if the job is waiting for sub-jobs.
            Exception: if the job is finished with a raised exception.
                This exception is the same as the original exception.
        """
        job_result = self._get_job_result(job_id)
        if job_result.result_type == JobResultType.RETURN:
            return job_result.deserialized()
        if job_result.result_type == JobResultType.RAISE:
            raise job_result.deserialized()
        raise Exception(job_result.detail)

    def poll(self, job_id: JobId, *, detail=False) -> Union[bool, JobStatus]:
        """Poll the status of a job.

        You can poll the status of a job by its job id.
        If the job is not finished, this function will return ``False``.
        You can use ``get`` to get the result of the job.

        Args:
            job_id: job id
            detail: if True, return the detail of the job status.

        Returns:
            If detail is False, return a bool:
                True if the job is finished successfully.
                False if the job is not finished.
            If detail is True, return a JobStatus:
                The status of the job.
        """
        if detail:
            return self._check_job_status(job_id)
        return self._check_job_status(job_id).is_success
