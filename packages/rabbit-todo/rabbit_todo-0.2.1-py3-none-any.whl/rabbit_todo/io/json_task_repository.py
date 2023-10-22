"""
JSON Task Repository

Main Class:
- JsonTaskRepository: Simple Json Task Repository.
                      Saves tasks to json file and loads tasks from json file.

Dependencies:
- rabbit_todo.core.i_task_repository: ITaskRepository class is base class of Json Task Repository.
- rabbit_todo.core.task: Task class.
- rabbit_todo.common.result: Result class used for error handling.
"""

# --- Standard Library ---
import json
from typing import Union

# --- First Party Library ---
from rabbit_todo.common.messages import ERROR_FILE_CORRUPTED
from rabbit_todo.common.messages import ERROR_NOT_FOUND
from rabbit_todo.common.result import Result
from rabbit_todo.core.i_task_repository import ITaskRepository
from rabbit_todo.core.task import Task
from rabbit_todo.io.file_handler import FileHandler
from rabbit_todo.io.io_config.json_config import INITIAL_TASKS_CONTENT
from rabbit_todo.io.io_config.json_config import TASKS_KEY


class JsonTaskRepository(ITaskRepository):
    """Saves tasks to json file and loads tasks from json file"""

    def __init__(self, file_handler: FileHandler, initial_content: str = INITIAL_TASKS_CONTENT):
        self._file_handler = file_handler
        self._file_handler.initialize(initial_content)

    def _load_json(self) -> Result[dict[str, list[dict[str, Union[int, bool, str]]]]]:
        try:
            with self._file_handler.open_file_r(TASKS_KEY) as file:
                content: dict[str, list[dict[str, Union[int, bool, str]]]] = json.load(file)
                return Result.ok(content)
        except json.decoder.JSONDecodeError:
            return Result.error(ERROR_FILE_CORRUPTED)

    def _save_tasks(self, tasks: list[Task]) -> None:
        content = {"tasks": [t.to_dict() for t in tasks]}
        with self._file_handler.open_file_w("tasks") as file:
            json.dump(content, file, indent=4, ensure_ascii=False)

    def get_all(self) -> Result[list[Task]]:
        return self._load_json().map(lambda data: [Task.from_dict(task) for task in data["tasks"]])

    def get_by_id(self, task_id: int) -> Result[Task]:
        # Get tasks
        result = self.get_all()
        if not result.is_success():
            return Result.error(result)
        tasks = result.unwrap()

        # Execute
        for task in tasks:
            if task.id == task_id:
                return Result.ok(task)

        return Result.error(ERROR_NOT_FOUND)

    def add(self, task: Task) -> Result[bool]:
        # Get tasks
        result = self.get_all()
        if not result.is_success():
            return Result.error(result)
        tasks = result.unwrap()

        # Execute
        tasks.append(task)

        # Save
        self._save_tasks(tasks)

        return Result.ok(True)

    def remove(self, task: Task) -> Result[bool]:
        # Get tasks
        result = self.get_all()
        if not result.is_success():
            return Result.error(result)
        tasks = result.unwrap()

        # Execute
        for task_ in tasks[:]:
            if task_.id == task.id:
                tasks.remove(task_)
                self._save_tasks(tasks)
                return Result.ok(True)

        return Result.error(ERROR_NOT_FOUND)

    def update(self, task: Task) -> Result[bool]:
        # Get tasks
        result = self.get_all()
        if not result.is_success():
            return Result.error(result)
        tasks = result.unwrap()

        # Execute
        for task_ in tasks[:]:
            if task_.id == task.id:
                idx = tasks.index(task_)
                tasks[idx] = task
                self._save_tasks(tasks)
                return Result.ok(True)

        return Result.error(ERROR_NOT_FOUND)
