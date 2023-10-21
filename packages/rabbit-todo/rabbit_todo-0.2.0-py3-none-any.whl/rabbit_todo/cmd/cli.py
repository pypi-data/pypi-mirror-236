# --- Standard Library ---
import sys

# --- Third Party Library ---
import click

# --- First Party Library ---
from rabbit_todo.common.messages import SuccessMessage
from rabbit_todo.core.task import Task
from rabbit_todo.core.task_id_generator import TaskIdGenerator
from rabbit_todo.io.json_task_repository import JsonTaskRepository


def exit_with_error(message: str) -> None:
    print(message)
    sys.exit(1)


@click.group
def cli() -> None:  # TODO: Refactoring there codes
    pass


@cli.command("add")
@click.argument("task-name", type=click.STRING)
def add_task(task_name: str) -> None:
    repo = JsonTaskRepository()

    # Create task instance
    generator = TaskIdGenerator(repo)
    result = generator.next_id()
    if not result.is_success:
        exit_with_error(result.message)
    next_id = result.unwrap()
    task = Task(next_id, task_name)

    # Execute
    result = repo.add(task)
    if result.is_success():
        print(SuccessMessage.add_task(task_name))
    else:
        exit_with_error(result.message)


@cli.command("remove")
@click.argument("task-id", type=click.INT)
def remove_task(task_id: int) -> None:
    repo = JsonTaskRepository()

    # Get task instance
    result = repo.get_by_id(task_id)
    if not result.is_success():
        exit_with_error(result.message)
    task = result.unwrap()

    # Execute
    result = repo.remove(task)
    if result.is_success():
        print(SuccessMessage.remove_task(task.name))
    else:
        exit_with_error(result.message)


@cli.command("done")
@click.argument("task-id", type=click.INT)
def done_task(task_id: int) -> None:
    repo = JsonTaskRepository()

    # Get task instance
    result = repo.get_by_id(task_id)
    if not result.is_success():
        exit_with_error(result.message)
    task = result.unwrap()

    # Execute
    task.mark_as_complete()
    result = repo.update(task)
    if result.is_success():
        print(SuccessMessage.mark_as_complete(task.name))
    else:
        exit_with_error(result.message)


@cli.command("list")
def list_task() -> None:
    repo = JsonTaskRepository()

    # Get task instances
    result = repo.get_all()
    if not result.is_success():
        exit_with_error(result.message)
    tasks = result.unwrap()

    # Execute
    for task in tasks:
        completed_mark = "[X]" if task.completed else "[ ]"
        print(f"{completed_mark}: ID -{task.id:^3}  {task.name}")
