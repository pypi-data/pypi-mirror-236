import click

from todotree.Config import Config
from todotree.Errors.DoneFileNotFound import DoneFileNotFound
from todotree.Errors.TodoFileNotFound import TodoFileNotFound
from todotree.Taskmanager import Taskmanager


class Revive:
    def __init__(self, config: Config, task_manager: Taskmanager):
        self.taskManager = task_manager
        self.config = config

    def run(self, done_number: int):
        try:
            click.echo(self.taskManager.revive_task(done_number))
        except TodoFileNotFound as e:
            e.echo_and_exit(self.config)
        except DoneFileNotFound as e:
            e.echo_and_exit(self.config)
        self.config.git.commit_and_push("revive")
