from typing import Tuple

import click

from todotree.Config import Config
from todotree.Errors.TodoFileNotFound import TodoFileNotFound
from todotree.Taskmanager import Taskmanager


class Add:
    def __init__(self, config: Config, task_manager: Taskmanager):
        self.taskManager = task_manager
        self.config = config

    def run(self, task: Tuple):
        # Convert tuple to string
        task: str = " ".join(map(str, task))
        try:
            # Disable fancy imports, because they are not needed.
            self.config.enable_project_folder = False
            # Import tasks.
            self.taskManager.import_tasks()
            # Add task
            new_number = self.taskManager.add_task_to_file(task.strip() + "\n")
            self.config.console.info("Task added:")
            click.echo(f"{new_number} {task}")
            self.config.git.commit_and_push("add")
        except TodoFileNotFound as e:
            e.echo_and_exit(self.config)
