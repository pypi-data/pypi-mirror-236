"""
Result class

MainClass
- Result: Contains value or error message.
          This class is used for error handling.

Dependencies:
    This class doesn't have any dependencies.

Note:
    This class is implemented similarly to the `Result` type in Rust.
"""

from __future__ import annotations

# --- Standard Library ---
from typing import Callable
from typing import Generic
from typing import TypeVar

T = TypeVar("T")
B = TypeVar("B")
V = TypeVar("V")


class Result(Generic[T]):
    """Contains value or error message"""

    def __init__(self, value: T | None, error_message: str | None = None) -> None:
        self._value = value
        self._message = error_message

    @classmethod
    def ok(cls, value: T) -> Result[T]:
        """Constructs the result with the given value."""
        return cls(value=value)

    @classmethod
    def error(cls, message_or_result: str | Result[B]) -> Result[T]:
        """Constructs the result with the given error message or the result."""
        if isinstance(message_or_result, str):
            return Result(value=None, error_message=message_or_result)
        if isinstance(message_or_result, Result):
            return Result(value=None, error_message=message_or_result.message)

        raise TypeError(message_or_result)

    @property
    def message(self) -> str:
        """Returns the error message if it exists."""
        return self._message or "Unknown error occurred."

    def is_success(self) -> bool:
        """Returns true if the result is success otherwise false."""
        return self._value is not None

    def map(self, func: Callable[[T], V]) -> Result[V]:
        """
        Applies the given function to the result's value if it's a success.
        If it's an error, return a new Result with the same error message.
        """
        if self.is_success():
            assert self._value is not None
            return Result(value=func(self._value), error_message=None)
        return Result(value=None, error_message=self._message or "Unknown error occurred.")

    def unwrap(self) -> T:
        """Retrieves the value from the result. If not success, raises a RuntimeError."""
        if not self.is_success():
            raise RuntimeError("Result is not a success")
        assert self._value is not None
        return self._value
