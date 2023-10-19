from typing import Optional

import click

from todotree.ConsolePrefixes import ConsolePrefixes


class ConsolePrefixesInit(ConsolePrefixes):
    """
    Provides additional features to ConsolePrefixes.
    These are only used in the Init command.
    """
    def __init__(self, enable_colors: bool,
                 console_good: str, console_warn: str, console_error: str,
                 console_info_color: str, console_warn_color: str, console_error_color: str):
        super().__init__(enable_colors,
                         console_good, console_warn, console_error,
                         console_info_color, console_warn_color, console_error_color)
        self.enable_colors = enable_colors
        self.console_error = console_error
        self.console_warn = console_warn
        self.console_info = console_good
        self.console_info_color = console_info_color
        self.console_warn_color = console_warn_color
        self.console_error_color = console_error_color

    @staticmethod
    def from_console_prefixes(c: ConsolePrefixes):
        """Converts from console prefixes."""
        return ConsolePrefixesInit(
            enable_colors=c.enable_colors,
            console_good=c.console_info,
            console_warn=c.console_warn,
            console_error=c.console_error
        )

    def prompt_menu(self, question: str, answers: list, custom_answer: Optional[str] = None) -> str | int:
        """
        Ask the end user for input using a menu.
        @param question: The question to ask the user.
        @param answers: The predefined answers that the user can select.
        @param custom_answer: The custom option Text. Do not append with a dot.
            If the user chooses the Custom answer option. The user will be prompted to fill in the custom answer.
        @return: The answer that the user chose.
        If the user chooses a predefined option, it will be number of that option.
        It will be a string if the answer came from the custom option.
        """
        text = question + "\n"
        for i, answer in enumerate(answers):
            text += f"  [{i}]  {str(answer)} \n"
        # `i` is now the length of the answers list.
        custom_number = len(answers)
        if custom_answer:
            text += f"  [{custom_number}]  {custom_answer}. \n"

        choices = [str(i) for i in range(0, custom_number + 1)]
        answer_int = int(self.prompt(text=text, show_choices=False, type=click.Choice(choices)))
        if custom_answer and answer_int == custom_number:
            answer = self.prompt(text=f"{custom_answer} option chosen. Please type it in.")
            self.confirm(text=f"Is this correct?: {answer}")
            return answer
        else:
            self.confirm(text=f"Is this correct?: {answers[answer_int]}")
            return answer_int

    def prompt(self, *args, **kwargs):
        """Wrapper for click.prompt"""
        self._emit_prefix(self.console_warn_color, self.console_warn)
        return click.prompt(*args, **kwargs)

    def confirm(self, *args, **kwargs):
        """Wrapper for click.confirm"""
        self._emit_prefix(self.console_warn_color, self.console_warn)
        return click.confirm(*args, **kwargs)
