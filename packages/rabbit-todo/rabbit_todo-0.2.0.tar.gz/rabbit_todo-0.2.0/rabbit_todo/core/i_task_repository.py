"""
ITaskRepository class.

Main Class:
- ITaskRepository: The abstract base class for all Task Repositories.

Dependencies:
- rabbit_todo.core.task: task class to be instantiated from ITaskRepository.
- rabbit_todo.common.result: Result class used for error handling.
"""

# --- Standard Library ---
from abc import ABC
from abc import abstractmethod

# --- First Party Library ---
from rabbit_todo.common.result import Result
from rabbit_todo.core.task import Task


class ITaskRepository(ABC):
    """Abstract base class for all Task Repositories"""

    @abstractmethod
    def get_all(self) -> Result[list[Task]]:
        """Get all tasks."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, task_id: int) -> Result[Task]:
        """Get the task by id."""
        raise NotImplementedError

    @abstractmethod
    def add(self, task: Task) -> Result[bool]:
        """Add the task to the repository."""
        raise NotImplementedError

    @abstractmethod
    def remove(self, task: Task) -> Result[bool]:
        """Remove the task from the repository."""
        raise NotImplementedError

    @abstractmethod
    def update(self, task: Task) -> Result[bool]:
        """Update the task in the repository."""
        raise NotImplementedError
