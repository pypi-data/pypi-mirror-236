# --- Standard Library ---
import json

# --- First Party Library ---
from rabbit_todo.common.messages import ERROR_FILE_CORRUPTED
from rabbit_todo.common.messages import ERROR_NOT_FOUND
from rabbit_todo.common.result import Result
from rabbit_todo.core.i_task_repository import ITaskRepository
from rabbit_todo.core.task import Task


class JsonTaskRepository(ITaskRepository):
    def __init__(self, file_path: str = "tasks.json"):
        self.file_path = file_path
        self.content: dict[str, list[dict[str, int | bool | str]]] = {"tasks": []}

    def _load_json(self) -> Result[dict[str, list[dict[str, int | bool | str]]]]:
        try:
            with open(self.file_path, "r") as file:
                self.content = json.load(file)
                return Result.ok(self.content)
        except FileNotFoundError:
            return Result.ok(self.content)
        except json.decoder.JSONDecodeError:
            return Result.error(ERROR_FILE_CORRUPTED)

    def _save_tasks(self, tasks: list[Task]) -> None:
        with open(self.file_path, "w") as file:
            self.content["tasks"] = [t.to_dict() for t in tasks]
            json.dump(self.content, file, indent=4, ensure_ascii=False)

    def get_all(self) -> Result[list[Task]]:
        # Get data
        result = self._load_json()
        if not result.is_success():
            return Result.from_result(result)
        data = result.unwrap()

        # Execute
        task_data = data["tasks"]
        tasks = [Task.from_dict(task) for task in task_data]

        return Result.ok(tasks)

    def get_by_id(self, task_id: int) -> Result[Task]:
        # Get tasks
        result = self.get_all()
        if not result.is_success():
            return Result.from_result(result)
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
            return Result.from_result(result)
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
            return Result.from_result(result)
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
            return Result.from_result(result)
        tasks = result.unwrap()

        # Execute
        for task_ in tasks[:]:
            if task_.id == task.id:
                idx = tasks.index(task_)
                tasks[idx] = task
                self._save_tasks(tasks)
                return Result.ok(True)

        return Result.error(ERROR_NOT_FOUND)
