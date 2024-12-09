from rich.console import Console
from rich.panel import Panel
from rich.text import Text


class APIError(Exception):
    def __init__(self, message: str = None, do_rich_print: bool = True):
        super().__init__(message)
        self.message = message
        if do_rich_print:
            console = Console()
            error_message = Text(self.message, style="bold red")
            error_panel = Panel(error_message, expand=False)
            console.print(error_panel)

    def __str__(self):
        return self.message


class APIStatusError(APIError):
    pass
