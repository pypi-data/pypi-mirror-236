from __future__ import annotations

from typing import Any


class Task:
    def __init__(self, id: int, name: str):
        self._id = id
        self._name = name
        self._completed = False

    @classmethod
    def from_dict(cls, data: dict[str, int | str | bool]) -> Task:  # FIXME ADD ERROR HANDLING
        instance = cls(data["id"], data["name"])
        instance._completed = data["completed"]
        return instance

    def to_dict(self) -> dict[str, int | str | bool]:
        return {
            "id"       : self._id,
            "name"     : self._name,
            "completed": self._completed
        }

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def completed(self) -> bool:
        return self._completed

    def mark_as_complete(self) -> None:
        self._completed = True

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Task):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
