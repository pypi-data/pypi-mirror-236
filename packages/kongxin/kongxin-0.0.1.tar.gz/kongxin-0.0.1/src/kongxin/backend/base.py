"""Base backend for kongxin.

This module contains the base backend for kongxin,
which is an abstract class that defines the interface of a backend.
"""

import abc
from typing import Optional

from kongxin.types import JobId, JobQuest, JobQuestExecution, JobResult, JobStatus


class BaseBackendABC(abc.ABC):
    """Base backend for kongxin.

    This is an abstract class that defines the interface of a backend.

    You can implement your own backend by inheriting this class.
    """

    @abc.abstractmethod
    def add_job(self, job_quest: JobQuest) -> bool:
        """Add job to queue.

        Add a job quest to the queue.
        If the job quest is already in the queue, do nothing.

        Args:
            job_quest (JobQuest): The job quest to be added.

        Returns:
            bool: True if the job quest is added.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_next_job_quest(self) -> Optional[JobQuestExecution]:
        """Get next job quest.

        Get next job quest and mark it as in progress
        Returns None if no job quest is available
        Otherwise returns the job quest execution

        Returns:
            Optional[JobQuestExecution]: The job quest execution to be executed.
                None if no job quest is available.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def put_job_result(self, job_exec: JobQuestExecution, job_result: JobResult):
        """Put job result of the job quest execution.

        Put job result of the job quest execution

        Args:
            job_exec (JobQuestExecution): The job quest execution.
            job_result (JobResult): The job result.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def update_job_status(self, job_exec: JobQuestExecution, job_status: JobStatus):
        """Update job status of the job quest execution.

        Args:
            job_exec (JobQuestExecution): The job quest execution.
            job_status (JobStatus): The job status.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_children(self, job_id: JobId) -> list[JobId]:
        """Get all children of a job.

        Args:
            job_id (JobId): the parent job id

        Returns:
            list[JobId]: The list of all children job ids.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_job_todo(self, job_id: JobId, *, set_as: bool) -> bool:
        """Set job todo.

        Args:
            job_id (JobId): The job id.
            set_as (bool): Set job as to-do or not.

        Returns:
            bool: True if the job's to-do-ness is changed.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def check_job_status(self, job_id: JobId) -> JobStatus:
        """Check job status.

        Check job status of the job quest execution
        Should always return a valid job status.
        For example, if job is not found, return a pending job status.

        Args:
            job_id (JobId): The job id.

        Returns:
            JobStatus: The job status.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_job_result(self, job_id: JobId) -> Optional[JobResult]:
        """Get job result.

        Get job result of the job quest execution
        Caller should check job status first.
        Returns None if job result is not available

        Args:
            job_id (JobId): The job id.

        Returns:
            Optional[JobResult]: The job result.
                None if job result is not available.
        """
        raise NotImplementedError
