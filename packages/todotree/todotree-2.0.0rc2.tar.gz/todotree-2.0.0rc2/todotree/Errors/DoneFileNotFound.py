from todotree.Config import Config


class DoneFileNotFound(BaseException):
    """
    Represents an error indicating that the done.txt file is not found.
    """
    def echo_and_exit(self, config: Config):
        config.console.error("The done.txt could not be found.")
        config.console.error(f"It searched at the following location: {config.done_file}")
        config.console.verbose(self)
        exit(1)
