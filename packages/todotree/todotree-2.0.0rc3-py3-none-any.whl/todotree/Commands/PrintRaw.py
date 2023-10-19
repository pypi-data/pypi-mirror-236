import click

from todotree.Config import Config
from todotree.Errors.TodoFileNotFound import TodoFileNotFound
from todotree.Taskmanager import Taskmanager


class PrintRaw:
    def __init__(self, config: Config, task_manager: Taskmanager):
        self.taskManager = task_manager
        self.config = config

    def run(self):
        try:
            with open(self.taskManager.config.todo_file, "r") as f:
                click.echo(f.read())
        except FileNotFoundError:
            TodoFileNotFound().echo_and_exit(self.config)

