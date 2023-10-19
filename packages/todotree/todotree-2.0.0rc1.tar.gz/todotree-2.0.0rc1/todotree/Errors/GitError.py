from todotree.ConsolePrefixes import ConsolePrefixes


class GitError(BaseException):
    """
    Represents an error indicating that something is wrong with the git repo.
    """
    def warn_and_continue(self, console: ConsolePrefixes):
        console.warning("An error occurred while trying to git clone.")
        console.warning("If this was unexpected, try again with the --verbose flag.")


