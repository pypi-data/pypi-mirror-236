from todotree.Config import Config
from todotree.Errors.TodoFileNotFound import TodoFileNotFound
from todotree.Taskmanager import Taskmanager


class Priority:
    def __init__(self, config: Config, task_manager: Taskmanager):
        self.taskManager = task_manager
        self.config = config

    def run(self, task_number: int, new_priority: str):
        # Disable fancy imports.
        self.config.enable_project_folder = False
        # Run task.
        try:
            self.taskManager.import_tasks()
        except TodoFileNotFound as e:
            e.echo_and_exit(self.config)
        self.taskManager.add_or_update_priority(
            priority=(new_priority.upper()), task_number=task_number)
