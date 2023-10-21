"""Backend for kongxin.

A backend is a storage for kongxin.

Yuo can use the default backend or set your own backend.
Just call `set_default_backend` to set the default backend.
"""

__all__ = ["set_default_backend", "default_backend"]

from typing import Literal

from kongxin.backend.filesystem_backend import FileSystemBackend
from kongxin.exception import NotSupported

default_backend = None


def set_default_backend(backend: Literal["filesystem"]):
    """Set the default backend.

    Args:
        backend (Literal["filesystem"]): The backend to be set.

    Raises:
        NotSupported: If the backend is not supported.
    """
    global default_backend
    if backend == "filesystem":
        default_backend = FileSystemBackend.singleton()
    else:
        raise NotSupported(f"backend:{backend} is not supported")


set_default_backend("filesystem")
