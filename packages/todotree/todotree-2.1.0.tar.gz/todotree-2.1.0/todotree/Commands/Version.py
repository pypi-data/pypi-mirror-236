import importlib

from todotree.Config import Config
from todotree.Taskmanager import Taskmanager


class Version:

    def __init__(self, config: Config, task_manager: Taskmanager):
        self.taskManager = task_manager
        self.config = config

    def run(self):
        version = importlib.metadata.version("todotree")
        if self.config.console.is_verbose():
            self.config.console.verbose(f"The version is {version}")
        elif self.config.console.is_quiet():
            self.config.console.warning(version)
        else:
            self.config.console.info(f"Version: {version}")
