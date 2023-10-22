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
from datetime import datetime
from typing import Any


def _check_str_key(data: dict[str, Any], key: str) -> str:
    value = data.get(key, None)
    if not isinstance(value, str):
        raise ValueError(f"Invalid type for {key}")
    return value


class Task:
    """Represents a single task"""

    def __init__(
        self,
        id_: int,
        name: str,
        notes: str = "",
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        self._id = id_
        self._name = name
        self._notes = notes
        self._completed = False
        self._created_at = created_at if created_at else datetime.now().replace(microsecond=0)
        self._updated_at = updated_at if updated_at else datetime.now().replace(microsecond=0)

    @classmethod
    def from_dict(cls, data: dict[str, int | str | bool]) -> Task:
        """Instantiates a Task from a dictionary"""
        try:
            id_ = int(data["id"])
            name = str(data["name"])
            completed = bool(data["completed"])
            notes = str(data["notes"])
            created_at = datetime.strptime(_check_str_key(data, "created_at"), "%Y-%m-%d %H:%M:%S")
            updated_at = datetime.strptime(_check_str_key(data, "updated_at"), "%Y-%m-%d %H:%M:%S")
        except (TypeError, KeyError, ValueError) as e:
            raise ValueError(f"Invalid data for creating a Task: {e}") from e

        instance = cls(id_, name, notes=notes, created_at=created_at, updated_at=updated_at)
        instance._completed = completed
        return instance

    def to_dict(self) -> dict[str, int | str | bool | datetime]:
        """Converts the task to dictionary"""
        return {
            "id": self._id,
            "name": self._name,
            "completed": self._completed,
            "notes": self._notes,
            "created_at": self._created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self._updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

    @property
    def id(self) -> int:
        """Returns the id of the task"""
        return self._id

    @property
    def name(self) -> str:
        """Returns the name of the task"""
        return self._name

    @property
    def notes(self) -> str:
        """Returns the notes of the task"""
        return self._notes

    @property
    def completed(self) -> bool:
        """Returns whether the task is completed or not"""
        return self._completed

    @property
    def created_at(self) -> datetime:
        """Returns the date and time the task was created"""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """Returns the date and time the task was updated"""
        return self._updated_at

    def mark_as_complete(self) -> None:
        """Marks the task as complete"""
        self._completed = True

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Task):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
