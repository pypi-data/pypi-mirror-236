from pathlib import Path

import xdg_base_dirs

from todotree.Config import Config
from todotree.ConsolePrefixesInit import ConsolePrefixesInit


class Init:

    def __init__(self):
        self.config: Config = Config()
        """Configuration."""
        self.action_queue = []
        """List of actions to execute."""
        self.console: ConsolePrefixesInit = ConsolePrefixesInit.from_console_prefixes(self.config.console)

    def run(self):
        self.intro()
        is_git_cloned = False  # self.git_clone() implement.
        if not is_git_cloned:
            self.determine_console_prefixes()
            self.determine_config_location()
            self.determine_folder_location()
            self.enable_git()
            self.enable_project()
            self.example_todo()
            self.generate_config()
        # Write results of the answers to the locations.
        answer = self.console.prompt("Are you sure you want to write the config file?")
        if answer:
            self.config.write_config()

    def intro(self):
        self.console.info("This will configure todotree and generate the necessary files to run it.")
        self.console.info("If at any point you wish to stop, you can do so with Ctrl-C.")
        self.console.info("Also, all options can be changed afterwards in the config.yaml if you change your mind.")

    def determine_config_location(self):
        question = "Where do you want to store config.yaml?"
        answers = [
            Path(xdg_base_dirs.xdg_config_home() / "todotree" / "config.yaml"),
            Path(xdg_base_dirs.xdg_data_home() / "todotree" / "config.yaml")
        ]
        answer = self.console.prompt_menu(question, answers, "Custom location")
        if isinstance(answer, int):
            self.config.config_file = answers[answer]
        else:
            self.config.config_file = answer
            self.console.warning("Note: You need to supply todotree each time with the config location using "
                                 "--config-file")
            self.console.warning("It is advised to alias this in your profile for example in ~/.profile or $PROFILE.")
        self.console.info(f"Set the config location to {self.config.config_file}")

    def determine_console_prefixes(self):
        self.console.enable_colors = self.console.confirm(text="Do you want colors on your console?")
        question = "How do you want the decorations?"
        answers = [
            f"Default      | {self.console.console_info} | {self.console.console_warn} | {self.console.console_error} |"
            ,
            "Gentoo style |  *  |  *  |  *  |"
        ]
        answer = self.console.prompt_menu(question, answers)
        if answer == 1:
            # Then we set gentoo style.
            self.console.console_info, self.console.console_warn, self.console.console_error = ' * '

    def determine_folder_location(self):
        question = "Where do you want to store config.yaml?"
        answers = [
            Path(xdg_base_dirs.xdg_config_home() / "todotree" / "config.yaml"),
            Path(xdg_base_dirs.xdg_data_home() / "todotree" / "config.yaml")
        ]
        answer = self.console.prompt_menu(question, answers, "Custom location")
        if isinstance(answer, int):
            self.config.config_file = answers[answer]
        else:
            self.config.config_file = answer
            self.console.warning("Note: You need to supply todotree each time with the config location using "
                                 "--config-file")
            self.console.warning("It is advised to alias this in your profile i.e. (.profile or $PROFILE)")
        self.console.info(f"Set the config location to {self.config.config_file}")

    def enable_git(self):
        enable_git = self.console.confirm(text="Do you want to enable git?")
        if not enable_git:
            git_mode = "disabled"
        else:
            enable_remote = self.console.confirm(text="Do you want to work with a remote repo as well?")
            git_mode = "remote" if enable_remote else "local"
        self.config.git.git_mode = git_mode

    def example_todo(self):
        if self.console.confirm("Do you want to have your todo file filled with some examples?"):
            self.action_queue += "ExampleTodo"

    def enable_project(self):
        self.console.info("The project_directory functionality adds the projects in a given folder.")
        self.console.info("It will also add tasks if there is no task with the given project name in todo.txt,")
        self.console.info("reminding you that that project is stalled.")
        self.config.enable_project_folder = self.console.confirm(
            "Do you want to enable the project_directory functionality?")

        if self.config.enable_project_folder:
            self.config.project_tree_folder = self.console.prompt("What will the location of your projects be?",
                                                                  default=self.config.project_tree_folder)

    def generate_config(self):
        """Generate the example config with the chosen values."""
        pass

    def git_clone(self):
        answer = self.console.confirm("Do you already have an existing todotree folder on git?")
        if answer:
            self.console.prompt("Please enter the git clone url to clone from.")
            # FUTURE: implement git clone.
        return answer

