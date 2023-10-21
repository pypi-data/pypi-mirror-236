"""kongxin types."""
import datetime as dt
import uuid
from enum import Enum
from typing import Any, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class KongxinBaseType(BaseModel):
    """Base type for kongxin types."""


class KongxinBaseFrozenType(KongxinBaseType):
    """Base frozen type for kongxin types."""

    model_config = ConfigDict(frozen=True)


class ModelId(KongxinBaseFrozenType):
    """Model ID.

    TODO: Add more details after we have a clear picture of how to use this.
    """

    value: str
    pickled: Optional[bytes]

    def __str__(self):
        """Return string representation of the model ID."""
        return f"m:{self.value}"


class FunctionId(KongxinBaseFrozenType):
    """Function ID.

    Attributes:
        value: Function id.
        pickled: Pickled function. The pickler is specified by the task bank.
    """

    value: str
    pickled: Optional[bytes] = None

    def __str__(self):
        """Return string representation of the function ID."""
        return f"f:{self.value}"


class JobId(KongxinBaseFrozenType):
    """Job ID.

    Attributes:
        issue_time: Issue time of the job ID.
        func_id: Function ID.
        uuid: UUID of the job ID.
            The uuid is randomly generated for the root job.
            For sub-jobs, the uuid should be a hash of the job content and call stack.
            This is because we want to avoid duplicate sub-jobs,
            and we want to keep different sub-jobs have different job IDs.
            For example, sub-job id can be the hash of
            the function pickled, the arguments and the call stack.
    """

    issue_time: dt.datetime = Field(default_factory=dt.datetime.utcnow)
    func_id: FunctionId = Field(default_factory=FunctionId)
    uuid: UUID = Field(default_factory=uuid.uuid4)

    def __str__(self):
        """Return string representation of the job ID.

        Notes:
            Issue time is not included in the string representation,
            because when job with sub-jobs is retried,
            the issue time for the sub-job will be different.
            However, we want to keep the same job ID for the sub-job
            to avoid duplicate sub-jobs.
            Because only the first job ID will be used,
            the issue time is the first job ID is used.
        """
        return f"{self.func_id}:" f"job:{self.uuid}"


class ExecutionId(KongxinBaseFrozenType):
    """Execution ID.

    Attributes:
        issue_time: Issue time of the execution ID.
        job_id: Job ID.
        uuid: UUID of the execution ID.
    """

    issue_time: dt.datetime = Field(default_factory=dt.datetime.utcnow)
    job_id: JobId = Field(default_factory=JobId)
    uuid: UUID = Field(default_factory=uuid.uuid4)

    def __str__(self):
        """Return string representation of the execution ID."""
        return (
            f"{self.job_id.func_id}:"
            f"t:{self.issue_time.strftime('%Y%m%dT%H%M%S')}:"
            f"job:{self.job_id.uuid}:"
            f"exe:{self.uuid}"
        )


class JobQuest(KongxinBaseFrozenType):
    """Job quest.

    Attributes:
        job_id: Job ID.
        func_id: Function ID.
        args: Arguments of the function.
        kwargs: Keyword arguments of the function.
        parent_job_id (Optional[JobId]): the id of its parent job.
            Should be None if this is the root job (i.e., no parent).
    """

    job_id: JobId
    func_id: FunctionId
    args: tuple
    kwargs: dict[str, Any]
    parent_job_id: Optional[JobId]


class JobQuestExecution(KongxinBaseFrozenType):
    """Job quest execution.

    Attributes:
        exec_id: Execution ID.
        job_quest: Job quest.
    """

    exec_id: ExecutionId
    job_quest: JobQuest


class JobStatusType(str, Enum):
    """Job status type.

    Note:
        The job status is updated by the job consumer.
        So when the job consumer is not running (e.g. the process dies),
        the job status will not be updated.

    Attributes:
        PENDING: After submitted and before dispatched.
            This is the initial state.
        DISPATCHED: After dispatched and before running.
        RUNNING: After running and before finished.
        WAITING: Suspended and waiting for sub-jobs.
            In this state, the result type is ``JobResultType.WAIT_SUBJOB``.
        SUCCESS: Finished successfully
            In this state, the result type is ``JobResultType.RETURN``.
        FAILED: Finished but failed.
            In this state, the result type is ``JobResultType.RAISE``.
        ERROR: Finished but with error.
            In this state, the result type is ``JobResultType.ERROR``.

    """

    PENDING = "PENDING"
    DISPATCHED = "DISPATCHED"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    ERROR = "ERROR"


class JobStatus(KongxinBaseFrozenType):
    """Job status.

    Note:
        The job status is updated by the job consumer.
        So when the job consumer is not running (e.g. the process dies),
        the job status will not be updated.

    Attributes:
        issue_time: Issue time of the job status.
        is_finished: Whether the job is finished.
        is_success: Whether the job is successful.
        state: State of the job.
        detail: Detail of the job.

    """

    issue_time: dt.datetime = Field(default_factory=dt.datetime.utcnow)
    is_finished: bool
    is_success: bool
    state: JobStatusType
    detail: str


class JobResultType(str, Enum):
    """Job result type.

    Attributes:
        RETURN: Returned successfully.
        RAISE: Raised exception.
        ERROR: Error occurred.
        WAIT_SUBJOB: Suspended and waiting for sub-jobs to finish.

    """

    RETURN = "RETURN"
    RAISE = "RAISE"
    ERROR = "ERROR"
    WAIT_SUBJOB = "WAIT_SUBJOB"


class SerializationMethodType(str, Enum):
    """Serialization method type.

    Attributes:
        PICKLE: Pickle, pickled by default pickler specified by the task bank.
        JSON: JSON, serialized by ``json.dumps`` and deserialized by ``json.loads``.
        PYDANTIC: Pydantic, serialized by ``pydantic.json.dumps``.
            The serialized result is a JSON string.
            However, when deserialized, the result is a Pydantic model.
    """

    PICKLE = "PICKLE"
    JSON = "JSON"
    PYDANTIC = "PYDANTIC"


class SerializationMethod(KongxinBaseFrozenType):
    """Serialization method.

    The serialization method is used to
    1. serialize the result of the job.
    2. deserialize the serialized result.

    Attributes:
        serializer: Serialization method type.
        is_bytes: Whether the serialized result is bytes.
        is_b64: Whether the serialized result is base64 encoded.
        pydantic_model: Pydantic model ID.

    """

    serializer: SerializationMethodType
    is_bytes: bool = Field(default=False)
    is_b64: bool = Field(default=True)
    pydantic_model: Optional[ModelId] = None  # TODO: check if this is needed


class JobResult(KongxinBaseFrozenType):
    """Job result.

    Attributes:
        issue_time: Issue time of the job result.
        result_type: Result type.
        serialized_result: Serialized result.
        serialization_method: Serialization method.
        detail: Detail of the job result.

    """

    issue_time: dt.datetime = Field(default_factory=dt.datetime.utcnow)
    result_type: JobResultType
    serialized_result: Union[str, bytes]
    serialization_method: SerializationMethod
    detail: str

    def deserialized(self):
        """Deserialize the serialized result.

        The result is saved as serialized, so we need to deserialize it before using it.
        The result is deserialized by the serialization method.

        Returns:
            Deserialized result.
        """
        from kongxin.serialization import deserialize

        return deserialize(self.serialized_result, method=self.serialization_method)
