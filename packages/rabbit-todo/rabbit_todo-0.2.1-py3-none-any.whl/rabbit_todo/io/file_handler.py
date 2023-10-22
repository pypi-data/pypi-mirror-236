"""
FileHandler
"""

# --- Standard Library ---
from contextlib import contextmanager
from pathlib import Path
from typing import Generator
from typing import TextIO

# --- First Party Library ---
from rabbit_todo.io.io_config.json_config import TASKS_FILE_NAME
from rabbit_todo.io.io_config.json_config import TASKS_KEY


class FileHandler:
    """Handles file and directory operations for the Rabbit-Todo application."""

    def __init__(self, root: Path) -> None:
        self._root = root
        self._tasks_path = root / TASKS_FILE_NAME

    def initialize(self, content: str) -> None:
        """Creates the required directory and files if they don't exist."""
        self._root.mkdir(parents=True, exist_ok=True)

        if not self._tasks_path.exists():
            with self.open_file_w("tasks") as f:
                f.write(content)

    @contextmanager
    def open_file_r(self, target: str) -> Generator[TextIO, None, None]:
        """Opens the file reading mode."""
        if target == TASKS_KEY:
            file = self._tasks_path.open(mode="r", encoding="utf-8")
            try:
                yield file
            finally:
                file.close()
        else:
            raise ValueError

    @contextmanager
    def open_file_w(self, target: str) -> Generator[TextIO, None, None]:
        """Opens the file writing mode."""
        if target == TASKS_KEY:
            file = self._tasks_path.open(mode="w", encoding="utf-8")
            try:
                yield file
            finally:
                file.close()
        else:
            raise ValueError

    def exists(self) -> bool:
        """Returns true if the directory exists, false otherwise."""
        return self._root.exists()
