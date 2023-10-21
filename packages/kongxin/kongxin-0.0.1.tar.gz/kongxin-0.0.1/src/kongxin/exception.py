"""This module defines exceptions used in kongxin."""

from kongxin.types import JobQuestExecution, JobStatus


class KongxinException(Exception):
    """Base exception for kongxin in public API.

    All public exceptions in kongxin should inherit from this class.
    """


class ProcessFinishedWithoutResult(KongxinException):
    """Process finished without result.

    This exception is raised when a process finished without result.
    """

    def __init__(self, job_quest_exec: JobQuestExecution):
        """Initialize ProcessFinishedWithoutResult exception."""
        super().__init__(str(job_quest_exec))
        self.job_quest_exec = job_quest_exec


class NotSupported(KongxinException):
    """Not supported.

    This exception is raised when a feature is not supported.

    When there's an option passed to a function, and the option is not supported,
    the function should raise this exception.

    For example,
    ```
    def func(option: str):

        if option == 'a':
            ...
        elif option == 'b':
            ...
        else:
            raise NotSupported(f'option:{option} is not supported')
    ```
    """


class NotFinished(KongxinException):
    """Not finished.

    This exception is raised when the job is not finished.

    For example, when you call ``kongxin.get`` on a job that is not finished,
    this exception will be raised.
    """

    def __init__(self, job_status: JobStatus):
        """Initialize NotFinished exception."""
        super().__init__(str(job_status))
        self.job_status = job_status


class KongxinBaseException(BaseException):
    """Base exception for kongxin in internal API.

    All internal exceptions in kongxin should inherit from this class.
    We need this class because
    we want users not to catch internal exceptions accidentally.

    For example, ``kongxin.get`` may raise ``kongxin.exception.WaitSubJobs``.
    If you catch ``Exception``, you will not catch ``kongxin.exception.WaitSubJobs``.

    ```
    try:
        kx.get(job_id)
    except Exception as e:
        print(e)  # not WaitSubJobs
    ```

    For ``WaitSubJobs``, user should not catch it.
    See ``kongxin.core.get`` for more details.
    """


class WaitSubJobs(KongxinBaseException):
    """Wait sub jobs.

    This exception is raised when a job is waiting for sub jobs to finished.
    """

    def __init__(self, job_status: JobStatus):
        """Initialize WaitSubJobs exception."""
        super().__init__(str(job_status))
        self.job_status = job_status
