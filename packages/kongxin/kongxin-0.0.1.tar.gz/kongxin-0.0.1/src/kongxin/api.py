"""The API module provides the public interface of kongxin."""

from typing import Callable, TypeVar

from typing_extensions import ParamSpec

from kongxin.core import Core

_core = Core.singleton()

_P = ParamSpec("_P")
_T = TypeVar("_T")


def _copy_signature(src_func: Callable[_P, _T]):
    """Copy the signature of the source function to the target function."""

    def _wrapper(tgt_func: Callable[_P, _T]) -> Callable[_P, _T]:
        def _wrapped_tgt_func(*args: _P.args, **kwargs: _P.kwargs) -> _T:
            tgt_func.__doc__ = src_func.__doc__
            return tgt_func(*args, **kwargs)

        return _wrapped_tgt_func

    return _wrapper


@_copy_signature(_core.submit)
def submit(*args, **kwargs):
    """Submit a job.

    See :meth:`kongxin.core.Core.submit` for details.
    """
    return _core.submit(*args, **kwargs)


@_copy_signature(_core.get)
def get(*args, **kwargs):
    """Get a job.

    See :meth:`kongxin.core.Core.get` for details.
    """
    return _core.get(*args, **kwargs)


@_copy_signature(_core.poll)
def poll(*args, **kwargs):
    """Poll a job.

    See :meth:`kongxin.core.Core.poll` for details.
    """
    return _core.poll(*args, **kwargs)
