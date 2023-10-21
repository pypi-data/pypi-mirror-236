"""
Entry-point for rabbit-todo Tool.

Main Function:
- main(): Initiates the command line interface for the rabbit-todo tool.

Dependencies:
- rabbit-todo.cmd: Provides command-line interface logic.

Usage:
    See the pyproject.toml scripts section for more information.
"""

# --- First Party Library ---
from rabbit_todo.cmd import cli


def main():
    """This is the entry point for the rabbit-todo."""
    cli()
