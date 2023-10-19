from abc import ABC, abstractmethod

from rabbit_todo.core.task import Task
from rabbit_todo.common.result import Result


class ITaskRepository(ABC):
    @abstractmethod
    def get_all(self) -> Result[list[Task]]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, task_id: int) -> Result[Task]:
        raise NotImplementedError

    @abstractmethod
    def add(self, task: Task) -> Result[bool]:
        raise NotImplementedError

    @abstractmethod
    def remove(self, task: Task) -> Result[bool]:
        raise NotImplementedError

    @abstractmethod
    def update(self, task: Task) -> Result[bool]:
        raise NotImplementedError
