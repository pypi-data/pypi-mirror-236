"""Bank module."""

__all__ = ["task_bank"]

from ._bank import TaskBank

task_bank = TaskBank.singleton()
