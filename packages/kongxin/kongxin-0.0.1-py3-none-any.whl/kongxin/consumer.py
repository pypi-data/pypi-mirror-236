"""This module contains the consumer daemon.

The consumer daemon is a process that consumes jobs from the backend.

Examples:
    To start the consumer daemon, run the following command in the terminal::

        TODO: make sure this is really the command to start the consumer daemon.
        $ python -m kongxin.consumer

    To stop the consumer daemon, press ``Ctrl+C`` in the terminal.
"""

import time

from kongxin.backend.base import BaseBackendABC
from kongxin.core import Core


def daemon(backend: BaseBackendABC):
    """Start the consumer daemon."""
    consumer = Core(backend)
    while True:
        if not consumer.consume():
            time.sleep(0.1)


if __name__ == "__main__":
    from kongxin.backend.filesystem_backend import FileSystemBackend

    daemon(FileSystemBackend())
