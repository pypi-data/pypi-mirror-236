from todotree.Config import Config


class TodoFileNotFound(BaseException):
    """
    Represents an error indicating that the todo.txt file is not found.
    """
    def echo_and_exit(self, config: Config):
        config.console.error("The todo.txt could not be found.")
        config.console.error(f"It searched at the following location: {config.todo_file}")
        config.console.verbose(str(self))
        exit(1)
