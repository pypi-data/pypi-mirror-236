from rabbit_todo.common.result import Result
from rabbit_todo.core.i_task_repository import ITaskRepository


class TaskIdGenerator:
    def __init__(self, repository: ITaskRepository) -> None:
        self._repository = repository

    def next_id(self) -> Result[int]:
        result = self._repository.get_all()
        if not result.is_success():
            return Result.from_result(result)

        tasks = result.unwrap()
        if not tasks:
            return Result.ok(0)

        max_id = max(task.id for task in tasks)
        return Result.ok(max_id + 1)
