import hashlib
import json
import uuid
from typing import Callable, Optional, Type, Union
from uuid import UUID

from pydantic import BaseModel

from kongxin.serialization import default_pickler
from kongxin.types import FunctionId, JobId, JobQuest, ModelId


def _try_convert_to_uuid(value) -> Optional[UUID]:
    if isinstance(value, UUID):
        return value
    try:
        return UUID(value)
    except (ValueError, TypeError):
        pass
    try:
        return UUID(bytes=value)
    except (ValueError, TypeError):
        pass
    try:
        return UUID(bytes_le=value)
    except (ValueError, TypeError):
        pass

    try:
        return UUID(fields=value)
    except (ValueError, TypeError):
        pass

    try:
        return UUID(int=value)
    except (ValueError, TypeError):
        pass
    return None


def _get_func_id(func_id: Union[FunctionId, UUID, str]) -> FunctionId:
    # try to convert func_id to FunctionId
    if isinstance(func_id, FunctionId):
        return func_id
    if (_uuid := _try_convert_to_uuid(func_id)) is not None:
        return FunctionId(value=str(_uuid))
    return FunctionId(value=str(func_id))


class _JobQuestBuilder:
    def __init__(
        self,
        func_id: FunctionId,
        parent: Optional[JobQuest] = None,
        last_job_quest: Optional[JobQuest] = None,
    ):
        self.func_id = func_id
        self.parent = parent
        self.last_job_quest = last_job_quest

    def __call__(self, *args, **kwargs):
        hash_key = {}

        if self.parent is not None:
            parent_job_id = self.parent.job_id
            hash_key["parent_job_id"] = str(parent_job_id)
        else:
            hash_key["root_random_id"] = str(uuid.uuid4())
            parent_job_id = None
        if self.last_job_quest is not None:
            hash_key["last_job_quest_id"] = str(self.last_job_quest.job_id)

        hash_key = tuple((k, hash_key[k]) for k in hash_key.keys())
        hashed_bytes = hashlib.sha1(json.dumps(hash_key).encode("utf-8")).digest()[:16]
        job_id = JobId(func_id=self.func_id, uuid=uuid.UUID(bytes=hashed_bytes))

        return JobQuest(
            job_id=job_id,
            func_id=self.func_id,
            args=args,
            kwargs=kwargs,
            parent_job_id=parent_job_id,
        )

    def __str__(self):
        """Return a string representation of this object."""
        return f"JobQuestBuilder(func_id={self.func_id})"

    def __repr__(self):
        return str(self)


class TaskBank:
    """Task bank."""

    _SINGLETON = None

    @classmethod
    def singleton(cls):
        """Get the singleton instance of TaskBank."""
        if cls._SINGLETON is None:
            cls._SINGLETON = cls()
        return cls._SINGLETON

    def __init__(self):
        """Initialize TaskBank."""
        self.__kongxin_id_to_func: dict[FunctionId, Callable] = {}
        self.__kongxin_func_to_id: dict[Callable, FunctionId] = {}

    @staticmethod
    def job_quest_by_id(
        func_id: str,
        parent: Optional[JobQuest] = None,
        last_job_quest: Optional[JobQuest] = None,
    ):
        """Get a job quest builder by its id."""
        func_id = _get_func_id(func_id)
        return _JobQuestBuilder(
            func_id,
            parent=parent,
            last_job_quest=last_job_quest,
        )

    def job_quest(
        self,
        func: Callable,
        parent: Optional[JobQuest] = None,
        last_job_quest: Optional[JobQuest] = None,
    ):
        """Get a job quest builder."""
        if func not in self.__kongxin_func_to_id:
            self._add(func)

        return _JobQuestBuilder(
            self.__kongxin_func_to_id[func],
            parent=parent,
            last_job_quest=last_job_quest,
        )

    def get_func(self, func_id: Union[FunctionId, UUID, str]) -> Callable:
        """Get a function by its id."""
        func_id = _get_func_id(func_id)
        if func_id in self.__kongxin_id_to_func:
            return self.__kongxin_id_to_func[func_id]
        if func_id.pickled is not None:
            func = default_pickler.loads(func_id.pickled)
            if callable(func):
                return func
        raise ValueError(f"Function id = '{func_id}' not registered")

    def _add(
        self, func: Callable, func_id: Optional[Union[FunctionId, UUID, str]] = None
    ):
        if not callable(func):
            raise ValueError(f"func:{func.__qualname__} is not callable")

        if func_id is None:
            pickled = default_pickler.dumps(func)
            _func_id = FunctionId(
                value=f"{hashlib.sha1(pickled).digest()[:16].hex()}",
                pickled=pickled,
            )
        else:
            _func_id = _get_func_id(func_id)

        # check if _func_id exists
        if _func_id in self.__kongxin_id_to_func:
            if self.__kongxin_id_to_func[_func_id] is not func:
                raise ValueError(f"Function id = '{_func_id}' already registered")

        # register func
        self.__kongxin_id_to_func[_func_id] = func
        self.__kongxin_func_to_id[func] = _func_id

        return func

    def add(self, func_id: Optional[Union[FunctionId, UUID, str]] = None):
        """Add a function to the task bank."""

        def _add(func: Callable):
            self._add(func, func_id)
            return func

        return _add


class ModelBank:
    """Model bank."""

    def __init__(self):
        """Initialize ModelBank."""
        self.__kongxin_models = {}

    def add(self, model_id: ModelId = None):
        """Add a model to the model bank."""

        def _add(model: Type[BaseModel]):
            if not issubclass(model, BaseModel):
                raise ValueError(
                    f"func:{model.__qualname__} is not a subclass of BaseModel"
                )
            nonlocal model_id
            if model_id is None:
                model_id = model.__qualname__
            if model_id in self.__kongxin_models:
                if self.__kongxin_models[model_id] is not model:
                    raise ValueError(f"Model id = '{model_id}' already registered")
            self.__kongxin_models[model_id] = model
            return model

        return _add
