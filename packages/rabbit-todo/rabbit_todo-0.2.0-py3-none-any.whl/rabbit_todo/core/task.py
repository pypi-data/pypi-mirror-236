"""
Task class.

Main Class:
- Task: Represents a single task.

Dependencies:
    This class doesn't have any dependencies.

Note:
    The identity of task classes managed by ID.
    Task classes with the same ID are considered the same.
"""

from __future__ import annotations

# --- Standard Library ---
from typing import Any


class Task:
    """Represents a single task"""

    def __init__(self, id_: int, name: str):
        self._id = id_
        self._name = name
        self._completed = False

    @classmethod
    def from_dict(cls, data: dict[str, int | str | bool]) -> Task:
        """Instantiates a Task from a dictionary"""
        instance = cls(data["id"], data["name"])
        instance._completed = data["completed"]
        return instance

    def to_dict(self) -> dict[str, int | str | bool]:
        """Converts the task to dictionary"""
        return {"id": self._id, "name": self._name, "completed": self._completed}

    @property
    def id(self) -> int:
        """Returns the id of the task"""
        return self._id

    @property
    def name(self) -> str:
        """Returns the name of the task"""
        return self._name

    @property
    def completed(self) -> bool:
        """Returns whether the task is completed or not"""
        return self._completed

    def mark_as_complete(self) -> None:
        """Marks the task as complete"""
        self._completed = True

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Task):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
