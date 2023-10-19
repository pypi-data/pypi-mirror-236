import click

from todotree.Config import Config
from todotree.Errors.TodoFileNotFound import TodoFileNotFound
from todotree.Taskmanager import Taskmanager


class List:
    def __init__(self, config: Config, task_manager: Taskmanager):
        self.taskManager = task_manager
        self.config = config

    def run(self):
        try:
            self.taskManager.import_tasks()
        except TodoFileNotFound as e:
            e.echo_and_exit(self.config)

        self.config.console.info("Todos")
        click.echo(self.taskManager)
