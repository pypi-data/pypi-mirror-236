# NOTE: this file cannot be in a class. See: https://github.com/pallets/click/issues/601
# https://click.palletsprojects.com/en/8.1.x/commands/#nested-handling-and-contexts

from pathlib import Path
from typing import List, Optional, Tuple

import click
# Commands are imported when the function is run, to increase performance.
from todotree.Addons import Addons
from todotree.Taskmanager import Taskmanager
from todotree.Config import Config
from todotree.MainUtils import MainUtils

# GLOBALS. #
config = Config()
addons = Addons(config)
taskManager = Taskmanager(config)


@click.group()
@MainUtils.common_options
def root(**kwargs):
    """
    The main list of todotree's command.

    The last option in the command will be in effect, so
       todotree --todo-file task.txt list --todo-file todo.txt
    will read from todo.txt and _not_ from task.txt
    """
    # ^ This text also shows up in the help command.
    # Parse options given before the command.
    # So the `--todo-file task.txt` option in the help text example.
    MainUtils.parse_common_options(config, **kwargs)


@root.command('add', short_help='Add a task to the task list')
@click.argument('task', type=str, nargs=-1)
@MainUtils.common_options
def add(task: Tuple, **kwargs):
    MainUtils.initialize(config, **kwargs)
    from todotree.Commands.Add import Add
    Add(config, taskManager).run(task)


@root.command('addx', short_help='Add a task and immediately mark it as done')
@click.argument('task', type=str, nargs=-1)
@MainUtils.common_options
def add_x(task: Tuple, **kwargs):
    """
    Adds a completed task to done.txt. The task is not added to todo.txt.
    :param task: The task to add to done.txt.
    """
    MainUtils.initialize(config, **kwargs)
    from todotree.Commands.AddX import AddX
    AddX(config, taskManager).run(task)


@root.command('append', short_help='append `append_string` to `task_nr`')
@click.argument('task_nr', type=int)
@click.argument('append_string', type=str, nargs=-1)
@MainUtils.common_options
def append(task_nr: int, append_string: Tuple[str], **kwargs):
    """
    Appends the contents of append_string to the task represented by task_nr.
    A space is inserted between the two tasks, so you do not have to worry that words aretogether.

    Example: todotree append 1 "some text"
    """
    MainUtils.initialize(config, **kwargs)
    from todotree.Commands.Append import Append
    Append(config, taskManager).run(task_nr, append_string)


@root.command('cd', short_help='print directory of the todo.txt directory')
@MainUtils.common_options
def cd(**kwargs):
    """print directory of the todo.txt directory"""
    MainUtils.initialize(config, **kwargs)
    from todotree.Commands.Cd import Cd
    Cd(config, taskManager).run()


@root.command('context', short_help='list task in a tree, by context')
@MainUtils.common_options
def context(**kwargs):
    """list a tree, of which the first node is the context, the second nodes are the tasks"""
    MainUtils.initialize(config, **kwargs)
    from todotree.Commands.Context import Context
    Context(config, taskManager).run()


@root.command('do', short_help='mark task as done and move it to the done.txt')
@click.argument('task_numbers', type=list, nargs=-1)  # type=list[int]
@MainUtils.common_options
def do(task_numbers: List[Tuple], **kwargs):
    """
    Mark tasks as done, therefor moving them to done.txt with a date stamp of today.
    :param task_numbers: The list of tasks which are completed.
    """
    MainUtils.initialize(config, **kwargs)
    from todotree.Commands.Do import Do
    Do(config, taskManager).run(task_numbers)


@root.command('due', short_help='List tasks by their due date')
@MainUtils.common_options
def due(**kwargs):
    """List tasks in a tree by their due date."""
    MainUtils.initialize(config, **kwargs)
    from todotree.Commands.Due import Due
    Due(config, taskManager).run()


@root.command('edit', short_help='open the todo.txt in an editor.')
@MainUtils.common_options
def edit(**kwargs):
    """
    Open the todo.txt in an editor for manual editing of tasks.
    This is useful when you need to modify a lot of tasks, which would be complicated when doing it with todotree.
    """
    MainUtils.initialize(config, **kwargs)
    from todotree.Commands.Edit import Edit
    Edit(config, taskManager).run()


@root.command('filter', short_help='only show tasks containing the search term.')
@click.argument('search_term')
@MainUtils.common_options
def filter_list(search_term, **kwargs):
    """
    Only show tasks which have search term in them. This can also be a keyword.

    :param search_term: The term to search.
    """
    MainUtils.initialize(config, **kwargs)
    from todotree.Commands.Filter import Filter
    Filter(config, taskManager).run(search_term)


@root.command('help', short_help='Print help text.')
@click.pass_context
def help_text(ctx: click.Context):
    print(ctx.parent.get_help())


@root.command('init', short_help='Initialize folder for first use.')
@MainUtils.common_options
def init(**kwargs):
    """
    Initializes the files and folders needed for a functioning todotree according to the user's prompts.
    """
    MainUtils.initialize(config, **kwargs)
    from todotree.Commands.Init import Init
    Init().run()


@root.command('list', short_help='List tasks')
@MainUtils.common_options
def list_tasks(**kwargs):
    """
    Print a flat list of tasks, sorted by their priority.
    """
    MainUtils.initialize(config, **kwargs)
    from todotree.Commands.List import List
    MainUtils.parse_common_options(config, **kwargs)
    List(config, taskManager).run()


@root.command('list_done', short_help='List tasks which are marked as done')
@MainUtils.common_options
def list_done(**kwargs):
    """
    List tasks which are marked as done. The numbers can be used with the revive command.
    """
    MainUtils.initialize(config, **kwargs)
    from todotree.Commands.ListDone import ListDone
    ListDone(config, taskManager).run()


@root.command('print_raw', short_help='print todo.txt without any formatting or filtering')
@MainUtils.common_options
def print_raw(**kwargs):
    """
    Output the todo.txt without any processing.
    This is equivalent to `cat $(todo cd)/todo.txt` in bash.
    """
    MainUtils.initialize(config, **kwargs)
    from todotree.Commands.PrintRaw import PrintRaw
    PrintRaw(config, taskManager).run()


@root.command('priority', short_help='set new priority to task')
@click.argument('task_number', type=int)
@click.argument('new_priority', type=str)
@MainUtils.common_options
def priority(task_number, new_priority, **kwargs):
    """
    Adds or updates the priority of the task.
    :param task_number: The task to re-prioritize.
    :param new_priority: The new priority.
    """
    MainUtils.initialize(config, **kwargs)
    from todotree.Commands.Priority import Priority
    Priority(config, taskManager).run(task_number, new_priority)


@root.command('project', short_help='print tree by project')
@MainUtils.common_options
def project(**kwargs):
    """
    Print the task list in a tree by project.
    """
    MainUtils.initialize(config, **kwargs)
    from todotree.Commands.Project import Project
    Project(config, taskManager).run()


@root.command('revive', short_help='Revive a task that was accidentally marked as done.')
@click.argument('done_number', type=int)
@MainUtils.common_options
def revive(done_number, **kwargs):
    """
    Move a task from done.txt to todo.txt.
    The `done_number` can be found using the `list_done` command.
    :param done_number: The number of the task to revive.
    """
    MainUtils.initialize(config, **kwargs)
    from todotree.Commands.Revive import Revive
    Revive(config, taskManager).run(done_number)


@root.command('schedule', short_help='hide task until date.')
@click.argument('task_number', type=int)
@click.argument('new_date', type=str, nargs=-1)
@MainUtils.common_options
def schedule(task_number: int, new_date: Tuple[str], **kwargs):
    """
    hide the task until the date given. If new_date is not in ISO format (yyyy-mm-dd) such as "Next Wednesday",
    then it tries to figure out the date with the `date` program, which is only in linux.
    """
    MainUtils.initialize(config, **kwargs)
    from todotree.Commands.Schedule import Schedule
    Schedule(config, taskManager).run(new_date, task_number)

@root.command('version')
@MainUtils.common_options
def version(**kwargs):
    MainUtils.initialize(config, **kwargs)
    from todotree.Commands.Version import Version
    Version(config, taskManager).run()

@root.command('addons', short_help='Run an addon script')
@click.argument('command', type=str)
@MainUtils.common_options
def addons_command(command: str, **kwargs):
    """
    Run an addon script.
    The script must be in the addons_folder. It can be any language you like: It does not have to be python.
    However, it must have the executable bit set.

    :param command: The script/command to run.
    """
    MainUtils.initialize(config, **kwargs)
    try:
        result = Addons(config).run(command)
    except FileNotFoundError:
        config.console.error(f"There is no script at {Path(config.addons_folder / command)}")
        exit(1)
    click.echo(result.stdout, nl=False)
    if result.returncode != 0:
        click.echo(result.stderr)
    config.git.commit_and_push(f"addons {command}")


#  End Region Command Definitions.
#  Setup Click

CONTEXT_SETTINGS: dict = dict(help_option_names=['-h', '--help'])
"""Click context settings. See https://click.palletsprojects.com/en/8.1.x/complex/ for more information."""
cli: click.CommandCollection = click.CommandCollection(
    sources=[root],
    context_settings=CONTEXT_SETTINGS
)
"""Command Collection defining defaults. https://click.palletsprojects.com/en/8.1.x/api/#click.CommandCollection ."""

if __name__ == '__main__':
    cli()
