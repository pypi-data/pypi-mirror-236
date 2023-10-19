import click

from todotree.Config import Config
from todotree.Taskmanager import Taskmanager


class Edit:
    def __init__(self, config: Config, task_manager: Taskmanager):
        self.taskManager = task_manager
        self.config = config

    def run(self):
        # Disable fancy imports.
        self.config.enable_project_folder = False
        click.edit(filename=str(self.config.todo_file))
        self.config.git.commit_and_push("edit")
