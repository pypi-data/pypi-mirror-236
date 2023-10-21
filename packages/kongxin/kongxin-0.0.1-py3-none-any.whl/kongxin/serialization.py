"""Serialization and Deserialization."""

import base64
import pickle
from typing import Union

from kongxin.exception import NotSupported
from kongxin.types import SerializationMethod, SerializationMethodType

default_pickler = pickle


def set_default_pickler(pickler):
    """Set the default pickler.

    Args:
        pickler: The pickler to be set.
            The pickler should have `dumps` and `loads` methods.
    """
    global default_pickler
    default_pickler = pickler


def _to_bytes(obj) -> bytes:
    if isinstance(obj, bytes):
        return obj
    if isinstance(obj, str):
        return obj.encode()
    raise TypeError(f"obj:{obj} is not bytes or str")


def serialize(obj, method: SerializationMethod) -> Union[str, bytes]:
    """Serialize an object to bytes or str.

    Args:
        obj: The object to be serialized.
        method: The serialization method.

    Returns:
        The serialized object.
    """
    if method.serializer == SerializationMethodType.PICKLE:
        s_bytes = default_pickler.dumps(obj)
    else:
        raise NotSupported(f"method:{method} is not supported")
    if method.is_b64:
        s_bytes = base64.b64encode(s_bytes)
    if not method.is_bytes:
        s_bytes = s_bytes.decode()
    return s_bytes


def deserialize(s_obj, method: SerializationMethod):
    """Deserialize an object from bytes or str.

    Args:
        s_obj: The serialized object.
        method: The serialization method.

    Returns:
        The deserialized object.
    """
    if not method.is_bytes:
        s_obj = _to_bytes(s_obj)
    if method.is_b64:
        s_obj = base64.b64decode(s_obj)
    if method.serializer == SerializationMethodType.PICKLE:
        return default_pickler.loads(s_obj)
    else:
        raise NotSupported(f"method:{method} is not supported")
