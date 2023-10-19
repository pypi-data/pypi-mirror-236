from typing import Tuple

import click

from todotree.Config import Config
from todotree.Errors.DoneFileNotFound import DoneFileNotFound
from todotree.Task.DoneTask import DoneTask
from todotree.Taskmanager import Taskmanager


class AddX:
    def __init__(self, config: Config, task_manager: Taskmanager):
        self.taskManager = task_manager
        self.config = config

    def run(self, task: Tuple):
        try:
            done = DoneTask.task_to_done(" ".join(map(str, task)))
            with self.config.done_file.open("a") as f:
                f.write(done)
            click.echo(done)
        except FileNotFoundError:
            DoneFileNotFound().echo_and_exit(self.config)
