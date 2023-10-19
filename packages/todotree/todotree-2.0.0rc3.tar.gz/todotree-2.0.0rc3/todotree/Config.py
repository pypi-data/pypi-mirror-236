from typing import Optional, Callable

from pathlib import Path

import xdg_base_dirs as xdg
from ruamel.yaml import YAML

from todotree.ConsolePrefixes import ConsolePrefixes
from todotree.Errors import ConfigFileNotFound
from todotree.GitHandler import GitHandler
from todotree.TreePrint import TreePrint


class Config:
    """
    The configuration of todotree.

    For a user guide, please refer to the content in `examples/config.yaml` instead.
    Not all values are mapped 1-to-1.
    """

    def __init__(self):
        #  Main variables.
        self.todo_folder: Path = xdg.xdg_data_home() / "todotree"
        """Path to the folder containing the data files."""

        self.project_tree_folder: Path = self.todo_folder / "projects"
        """Path to the folder containing the projects."""

        self.todo_file: Path = Path(self.todo_folder) / "todo.txt"
        """Path to the todo.txt file."""

        self.done_file: Path = Path(self.todo_folder) / "done.txt"
        """Path to the done.txt file."""

        self.config_file: Optional[Path] = None
        """Path to the config file."""

        self.addons_folder: Path = Path(self.todo_folder) / "addons"
        """Path to the addons folder."""

        # Features - Enables or disables certain features.
        self.enable_project_folder: bool = True
        """A value indicating whether to enable the project folder functionality."""

        #  Localization. #
        self.wishlistName: str = "wishlist"
        self.noProjectString: str = "No Project"
        self.noContextString: str = "No Context"
        self.emptyProjectString: str = "> (A) Todo: add next todo for this."

        #  Status Decorators.
        self.console: ConsolePrefixes = ConsolePrefixes(True, ' * ', ' ! ', '!!!',
                                                        'green', 'yellow', 'red')

        # Tree prints.
        self.tree_print: TreePrint = TreePrint(" ├──", " │  ", " └──", "    ")

        # Git functionality.
        self.git = GitHandler("disabled", 1, self.todo_folder, self.console)

        # Debug
        self.__yaml_object = None
        """Raw config object, for debugging."""

    def __str__(self):
        # Print each attribute in the list.
        s = "Configuration:\n"
        for item in self.__dict__:
            s += f"\t{item} = {self.__dict__[item]} \n"
        return s

    def read(self, path: Optional[Path] = None):
        """
        Loads the configuration from the given file at `path`.

        If empty, reads from default locations.
        """
        if path is not None:
            # print(f"Path is not None: {path}") # FUTURE: Verbose logging
            self.read_from_file(path)
            return
        # xdg compliant directory.
        if Path(xdg.xdg_config_home() / "todotree" / "config.yaml").exists():
            # print(f"Path is XDG Config") # FUTURE: Verbose logging
            self.read_from_file(Path(xdg.xdg_config_home() / "todotree" / "config.yaml"))
            return
        # xdg compliant directory if config file is considered "data".
        if Path(xdg.xdg_data_home() / "todotree" / "config.yaml").exists():
            # print(f"Path is XDG DATA") # FUTURE: Verbose logging
            self.read_from_file(Path(xdg.xdg_data_home() / "todotree" / "config.yaml"))
            return
        # No paths: use the defaults.
        return

    def read_from_file(self, file: Path):
        """Reads and parses yaml content from `file`."""
        self.config_file = file
        try:
            with open(file, 'r') as f:
                self._read_from_yaml(f.read())
        except FileNotFoundError as e:
            raise ConfigFileNotFound from e

    def _read_from_yaml(self, yaml_content: str):
        """Reads and overrides config settings defined in `yaml_content`."""
        # Convert yaml to python object.
        self.__yaml_object = YAML().load(yaml_content)
        if self.__yaml_object is None:
            return
        # Map each item to the self config.
        self.__section('main', self.__section_main)
        self.__section('paths', self.__section_paths)
        self.__section('localization', self.__section_localization)
        self.__section('decorators', self.__section_decorators)
        self.__section('tree', self.__section_tree)
        self.__section('git', self.__section_git)

    def __section(self, section_name: str, section_parser: Callable):
        """
        Checks if the section exists and passes it to the sub parser.
        """
        if self.__yaml_object.get(section_name) is not None:
            self.console.verbose(f"[{section_name}] section found, reading it.")
            # Parse the actual values.
            section_parser()
        else:
            self.console.verbose(f"[{section_name}] section not found, skipping it.")

    def __section_tree(self):
        self.tree_print.read_from_dict(self.__yaml_object['tree'])

    def __section_decorators(self):
        self.console.read_from_dict(self.__yaml_object['decorators'])

    def __section_localization(self):
        self.emptyProjectString = self.__yaml_object['localization'].get('empty_project', self.emptyProjectString)
        self.wishlistName = self.__yaml_object['localization'].get('wishlist_name', self.wishlistName)
        self.noProjectString = self.__yaml_object['localization'].get('no_project', self.noProjectString)
        self.noContextString = self.__yaml_object['localization'].get('no_context', self.noContextString)

    def __section_paths(self):
        self.todo_folder = Path(self.__yaml_object['paths'].get('folder', self.todo_folder)).expanduser()
        self.git.todo_folder = self.todo_folder

        self.todo_file = Path(
            self.__yaml_object['paths'].get('todo_file', Path(self.todo_folder) / "todo.txt")).expanduser()
        self.done_file = Path(
            self.__yaml_object['paths'].get('done_file', Path(self.todo_folder) / "done.txt")).expanduser()
        self.project_tree_folder = Path(
            self.__yaml_object['paths'].get('project_folder', self.project_tree_folder)).expanduser()
        self.addons_folder = Path(
            self.__yaml_object['paths'].get('addons_folder', self.addons_folder)).expanduser()

    def __section_main(self):
        self.enable_project_folder = self.__yaml_object['main'].get('enable_project_folder',
                                                                    self.enable_project_folder)

        # Postprocessing.
        if self.__yaml_object['main'].get("verbose", self.console.is_verbose()):
            self.console.set_verbose()
        if self.__yaml_object['main'].get("quiet", self.console.is_quiet()):
            self.console.set_quiet()

    def __section_git(self):
        self.git.read_from_dict(self.__yaml_object['git'])

    def write_config(self):
        """
        Writes the configuration file to the path specified in `self.config_file`
        """
        # Local import so that the file is not loaded in each time the program is started.
        from importlib import resources as import_resources
        from . import examples
        # https://stackoverflow.com/questions/6028000/how-to-read-a-static-file-from-inside-a-python-package
        example_config_path = (import_resources.files(examples) / "config.yaml")

        with example_config_path.open("r") as f:
            example_contents = f.read()

        yaml_structure = YAML().load(example_contents)
        # Change features.
        self.tree_print.apply_to_dict(yaml_structure['tree'])
        self.git.apply_to_dict(yaml_structure['git'])
        self.console.apply_to_dict(yaml_structure['decorators'])

        # Main.
        yaml_structure['main']['verbose'] = self.console.is_verbose()
        yaml_structure['main']['quiet'] = self.console.is_quiet()
        yaml_structure['main']['enable_project_folder'] = self.enable_project_folder
        # Paths.
        yaml_structure['paths']['folder'] = str(self.todo_folder)
        yaml_structure['paths']['todo_file'] = str(self.todo_file)
        yaml_structure['paths']['done_file'] = str(self.done_file)
        yaml_structure['paths']['project_folder'] = str(self.project_tree_folder)
        yaml_structure['paths']['addons_folder'] = str(self.addons_folder)
        # Localization.
        yaml_structure['localization']['wishlist_name'] = self.wishlistName
        yaml_structure['localization']['no_project'] = self.noProjectString
        yaml_structure['localization']['no_context'] = self.noContextString
        yaml_structure['localization']['empty_project'] = self.emptyProjectString

        # Write the file.
        Path(self.config_file).touch()
        write_yaml_settings = YAML()

        write_yaml_settings.dump(yaml_structure, stream=self.config_file)
