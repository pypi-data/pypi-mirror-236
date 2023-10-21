"""Filesystem backend for kongxin."""
import datetime as dt
import io
import os
import shutil
import time
from contextlib import contextmanager
from glob import glob
from typing import BinaryIO, Generator, Literal, Optional, Union
from zipfile import ZipFile

from overrides import override

from kongxin.backend.base import BaseBackendABC
from kongxin.exception import NotSupported
from kongxin.types import (
    ExecutionId,
    JobId,
    JobQuest,
    JobQuestExecution,
    JobResult,
    JobStatus,
    JobStatusType,
)


class _Locked(Exception):
    pass


@contextmanager
def _lock(lock_path: str, retry=False) -> None:
    while True:
        try:
            lock_fd = os.open(lock_path, os.O_CREAT | os.O_EXCL)
            yield
            os.close(lock_fd)
            os.remove(lock_path)
            break
        except FileExistsError:
            if not retry:
                raise _Locked()
            else:
                time.sleep(0.1)


def _touch(path):
    with open(path, "a"):
        os.utime(path, None)


class _Paths:
    def __init__(self, root_path):
        self.root_path = root_path

    def job_quest_dir(self, *, job_id: Union[JobId, str]) -> str:
        return f"{self.root_path}/job_quest/{job_id}"

    def job_quest_children_dir(self, *, job_id: Union[JobId, str]) -> str:
        return f"{self.job_quest_dir(job_id=job_id)}/children"

    def job_quest_children(
        self, *, parent_id: Union[JobId, str], child_id: Union[JobId, str]
    ) -> str:
        return f"{self.job_quest_dir(job_id=parent_id)}/children/{child_id}"

    def loop_job_quest_children(
        self, *, job_id: Union[JobId, str]
    ) -> Generator[str, None, None]:
        for child_path in glob(f"{self.root_path}/job_quest/{job_id}/children/*"):
            child_path, _, child_id = child_path.rpartition("/")
            yield child_id

    def job_quest_lock(
        self, *, job_id: Optional[Union[JobId, str]] = None, job_quest_dir=None
    ) -> str:
        if job_quest_dir is not None:
            return f"{job_quest_dir}/lock"
        assert job_id is not None
        return f"{self.job_quest_dir(job_id=job_id)}/lock"

    def job_quest_root(
        self, *, job_id: Optional[Union[JobId, str]] = None, job_quest_dir=None
    ) -> str:
        if job_quest_dir is not None:
            return f"{job_quest_dir}/root"
        assert job_id is not None
        return f"{self.job_quest_dir(job_id=job_id)}/root"

    def job_quest_todo(
        self, *, yesno, job_id: Optional[Union[JobId, str]] = None, job_quest_dir=None
    ) -> str:
        if job_quest_dir is not None:
            return f"{job_quest_dir}/todo.{yesno}"
        assert job_id is not None
        return f"{self.job_quest_dir(job_id=job_id)}/todo.{yesno}"

    def loop_job_quest_todo(self, *, yesno) -> Generator[str, None, None]:
        for job_path in glob(f"{self.root_path}/job_quest/*/todo.{yesno}"):
            job_path = job_path[: -len(f"/todo.{yesno}")]
            _, _, job_id_str = job_path.rpartition("/")
            yield job_id_str

    def exec_dir(
        self,
        *,
        job_id: Optional[Union[JobId, str]] = None,
        exec_id=None,
        job_quest_dir=None,
    ) -> str:
        if job_quest_dir is not None:
            return f"{job_quest_dir}/exec/{exec_id}"
        assert job_id is not None
        assert exec_id is not None
        return f"{self.root_path}/job_quest/{job_id}/exec/{exec_id}"

    def exec_lock(
        self,
        *,
        job_id: Optional[Union[JobId, str]] = None,
        exec_id=None,
        exec_dir: str = None,
    ) -> str:
        if exec_dir is not None:
            return f"{exec_dir}/lock"
        assert job_id is not None
        assert exec_id is not None
        return f"{self.exec_dir(job_id=job_id, exec_id=exec_id)}/lock"

    def exec_status(
        self,
        *,
        job_id: Optional[Union[JobId, str]] = None,
        exec_id=None,
        exec_dir: str = None,
    ) -> str:
        if exec_dir is not None:
            return f"{exec_dir}/status"
        assert job_id is not None
        assert exec_id is not None
        return f"{self.exec_dir(job_id=job_id, exec_id=exec_id)}/status"

    def exec_finished(
        self,
        *,
        yesno: str,
        job_id: Optional[Union[JobId, str]] = None,
        exec_id=None,
        exec_dir: str = None,
    ) -> str:
        if exec_dir is not None:
            return f"{exec_dir}/finished.{yesno}"
        assert job_id is not None
        assert exec_id is not None
        return f"{self.exec_dir(job_id=job_id, exec_id=exec_id)}/finished.{yesno}"

    def loop_exec_created_time(self, *, job_id: Union[JobId, str]) -> str:
        for exec_path in glob(
            f"{self.root_path}/job_quest/{job_id}/exec/*/created_time:*"
        ):
            exec_path, _, created_time = exec_path.rpartition("/")
            created_time = dt.datetime.strptime(
                created_time.replace("created_time:", ""), "%Y%m%dT%H%M%S.%f"
            )
            yield exec_path, created_time

    def exec_created_time(self, *, exec_dir):
        return (
            f"{exec_dir}/created_time:"
            f"{dt.datetime.utcnow().strftime('%Y%m%dT%H%M%S.%f')}"
        )

    def exec_result(self, *, exec_dir):
        return f"{exec_dir}/result"


class FileSystemBackend(BaseBackendABC):
    """Filesystem backend for kongxin.

    This backend is used for testing and debugging.
    Also, it can be used for production if you want to use a simple backend.

    """

    _SINGLETON = None

    @classmethod
    def singleton(cls):
        """Get the singleton instance of FileSystemBackend."""
        if cls._SINGLETON is None:
            cls._SINGLETON = cls()
        return cls._SINGLETON

    def __init__(
        self, root_path: str = "kongxin.db", serializer: Literal["pickle"] = "pickle"
    ):
        """Initialize FileSystemBackend.

        Args:
            root_path: The root path to store data.
            serializer: current only "pickle" is supported.
              The serializer used to serialize objects.
        """
        self.root_path = root_path
        self.serializer = serializer
        self.path = _Paths(root_path=root_path)
        os.makedirs(self.root_path, exist_ok=True)

    def _serialize(self, obj: Union[JobQuest, JobStatus, JobResult]) -> bytes:
        if self.serializer == "pickle":
            import pickle

            return pickle.dumps(obj)
        raise NotSupported(f"Serializer {self.serializer} not supported")

    def _deserialize(self, bio: BinaryIO) -> Union[JobQuest, JobStatus, JobResult]:
        if self.serializer == "pickle":
            import pickle

            return pickle.load(bio)
        raise NotSupported(f"Serializer {self.serializer} not supported")

    @override
    def add_job(self, job_quest: JobQuest) -> bool:
        # check if the job id already exists
        if os.path.exists(self.path.job_quest_dir(job_id=job_quest.job_id)):
            return False
        s_job_quest = self._serialize(job_quest)
        job_quest_dir = self.path.job_quest_dir(job_id=job_quest.job_id)
        os.makedirs(job_quest_dir, exist_ok=True)
        with open(self.path.job_quest_root(job_quest_dir=job_quest_dir), "wb") as f:
            f.write(s_job_quest)
        _touch(self.path.job_quest_todo(yesno="yes", job_quest_dir=job_quest_dir))
        # if the job has a parent, register this job_quest to its parent
        if job_quest.parent_job_id is not None:
            parent_children_dir = self.path.job_quest_children_dir(
                job_id=job_quest.parent_job_id
            )
            os.makedirs(parent_children_dir, exist_ok=True)
            with _lock(self.path.job_quest_lock(job_id=job_quest.parent_job_id)):
                _touch(
                    self.path.job_quest_children(
                        parent_id=job_quest.parent_job_id, child_id=job_quest.job_id
                    )
                )
        return True

    def _find_next_job_quest(self):
        for job_id_str in self.path.loop_job_quest_todo(yesno="yes"):
            if self.set_job_todo(job_id_str, set_as=False):
                return self.path.job_quest_dir(job_id=job_id_str)
        return None

    @override
    def get_next_job_quest(self) -> Optional[JobQuestExecution]:
        job_path = self._find_next_job_quest()
        if job_path is None:
            return None
        with open(self.path.job_quest_root(job_quest_dir=job_path), "rb") as f:
            job_quest = self._deserialize(f)
        job_exec = JobQuestExecution(
            exec_id=ExecutionId(job_id=job_quest.job_id), job_quest=job_quest
        )
        exec_path = self.path.exec_dir(job_quest_dir=job_path, exec_id=job_exec.exec_id)
        os.makedirs(exec_path, exist_ok=True)
        with _lock(self.path.exec_lock(exec_dir=exec_path), retry=True):
            with open(self.path.exec_status(exec_dir=exec_path), "wb") as f:
                f.write(
                    self._serialize(
                        JobStatus(
                            is_finished=False,
                            is_success=False,
                            state=JobStatusType.DISPATCHED,
                            detail="Job has been dispatched",
                        )
                    )
                )
            _touch(self.path.exec_finished(yesno="no", exec_dir=exec_path))
            _touch(self.path.exec_created_time(exec_dir=exec_path))
        return job_exec

    @override
    def update_job_status(self, job_exec: JobQuestExecution, job_status: JobStatus):
        exec_path = self.path.exec_dir(
            job_id=job_exec.job_quest.job_id, exec_id=job_exec.exec_id
        )
        s_job_status = self._serialize(job_status)
        with _lock(self.path.exec_lock(exec_dir=exec_path), retry=True):
            with open(self.path.exec_status(exec_dir=exec_path), "wb") as f:
                f.write(s_job_status)
            if job_status.is_finished:
                os.remove(self.path.exec_finished(yesno="no", exec_dir=exec_path))
                _touch(self.path.exec_finished(yesno="yes", exec_dir=exec_path))

    @override
    def get_all_children(self, job_id: JobId) -> list[JobId]:
        children = []
        for child_id in self.path.loop_job_quest_children(job_id=job_id):
            child_job_path = self.path.job_quest_dir(job_id=child_id)
            with open(
                self.path.job_quest_root(job_quest_dir=child_job_path), "rb"
            ) as f:
                child_job_quest = self._deserialize(f)
            children.append(child_job_quest.job_id)
        return children

    @override
    def set_job_todo(self, job_id: Union[JobId, str], *, set_as: bool) -> bool:
        from_todo = "yes" if not set_as else "no"
        to_todo = "yes" if set_as else "no"

        job_path = self.path.job_quest_dir(job_id=job_id)

        with _lock(self.path.job_quest_lock(job_quest_dir=job_path), retry=True):
            if not os.path.exists(
                self.path.job_quest_todo(yesno=from_todo, job_quest_dir=job_path)
            ):
                return False
            os.remove(self.path.job_quest_todo(yesno=from_todo, job_quest_dir=job_path))
            _touch(self.path.job_quest_todo(yesno=to_todo, job_quest_dir=job_path))
        return True

    @override
    def put_job_result(self, job_exec: JobQuestExecution, job_result: JobResult):
        exec_path = self.path.exec_dir(
            job_id=job_exec.job_quest.job_id, exec_id=job_exec.exec_id
        )
        s_job_result = self._serialize(job_result)
        with _lock(self.path.exec_lock(exec_dir=exec_path), retry=True):
            with open(self.path.exec_result(exec_dir=exec_path), "wb") as f:
                f.write(s_job_result)

    def _get_latest_exec_path(self, job_id: JobId) -> Optional[str]:
        created_times = {}
        for exec_path, created_time in self.path.loop_exec_created_time(job_id=job_id):
            created_times[exec_path] = created_time
        if not created_times:
            return None
        # use the latest exec
        return max(created_times, key=created_times.get)

    @override
    def check_job_status(self, job_id: JobId) -> JobStatus:
        job_status = JobStatus(
            is_finished=False,
            is_success=False,
            state=JobStatusType.PENDING,
            detail="Job has not been dispatched",
        )
        exec_path = self._get_latest_exec_path(job_id)
        if exec_path is None:
            return job_status
        with _lock(self.path.exec_lock(exec_dir=exec_path), retry=True):
            if not os.path.exists(self.path.exec_status(exec_dir=exec_path)):
                return job_status
            with open(self.path.exec_status(exec_dir=exec_path), "rb") as f:
                job_status = self._deserialize(f)
        return job_status

    @override
    def get_job_result(self, job_id: JobId) -> Optional[JobResult]:
        job_result = None
        exec_path = self._get_latest_exec_path(job_id)
        if exec_path is None:
            return job_result
        with _lock(self.path.exec_lock(exec_dir=exec_path), retry=True):
            if not os.path.exists(self.path.exec_result(exec_dir=exec_path)):
                return job_result
            with open(self.path.exec_result(exec_dir=exec_path), "rb") as f:
                job_result = self._deserialize(f)
        return job_result

    def dump_snapshot(self) -> io.BytesIO:
        """Dump snapshot of the backend.

        Returns:
            io.BytesIO: The snapshot in zip format.

        """
        bio = io.BytesIO()
        with ZipFile(bio, "w") as zip_file:
            for folder_name, _, filenames in os.walk(self.root_path):
                for filename in filenames:
                    file_path = os.path.join(folder_name, filename)
                    zip_file.write(file_path, file_path[len(self.root_path) + 1 :])
        bio.seek(0)
        return bio

    def load_snapshot(self, bio: io.BytesIO) -> None:
        """Load snapshot of the backend.

        Args:
            bio (io.BytesIO): The snapshot in zip format.
        """
        shutil.rmtree(self.root_path, ignore_errors=True)
        with ZipFile(bio, "r") as zip_file:
            zip_file.extractall(self.root_path)
