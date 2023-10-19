from todotree.Config import Config
from todotree.Errors.DoneFileNotFound import DoneFileNotFound
from todotree.Taskmanager import Taskmanager


class ListDone:
    def __init__(self, config: Config, task_manager: Taskmanager):
        self.taskManager = task_manager
        self.config = config

    def run(self):
        try:
            self.taskManager.list_done()
        except DoneFileNotFound as e:
            e.echo_and_exit(self.config)
