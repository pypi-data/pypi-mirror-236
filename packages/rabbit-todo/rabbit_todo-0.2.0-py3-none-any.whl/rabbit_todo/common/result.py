from __future__ import annotations

# --- Standard Library ---
from typing import Generic
from typing import TypeVar

T = TypeVar("T")
B = TypeVar("B")


class Result(Generic[T]):
    def __init__(self, value: T | None, is_success: bool, error_message: str | None = None) -> None:
        self._value = value
        self._is_success = is_success
        self._message = error_message

    @classmethod
    def ok(cls, value: T) -> Result[T]:
        return cls(value=value, is_success=True)

    @classmethod
    def error(cls, error_message: str) -> Result[T]:
        return cls(value=None, is_success=False, error_message=error_message)

    @classmethod
    def from_result(cls, result: Result[B]) -> Result[T]:
        if result.is_success():
            return cls.ok(result.unwrap())
        return cls.error(result.message)

    @property
    def message(self) -> str | None:
        return self._message

    def is_success(self) -> bool:
        return self._is_success

    def unwrap(self) -> T:
        if not self._is_success:
            raise RuntimeError("Result is not a success")
        return self._value
