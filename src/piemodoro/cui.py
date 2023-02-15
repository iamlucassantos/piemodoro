from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich.progress import Progress, BarColumn, SpinnerColumn, TextColumn
from datetime import datetime, timedelta
from rich.prompt import Prompt
from rich.console import Console


class Header:
    """Display header with clock."""

    def __init__(self, pomo):
        self.pomo = pomo

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            f"Pomos: {self.pomo.emoji()}",
            datetime.now().ctime().replace(":", "[blink]:[/]"),
        )
        return Panel(grid, title=":pie: [bold red]PieModoro[/bold red] :tomato:")


class Timer:
    """Display timer."""

    def __init__(self, pomo):
        self.pomo = pomo
        self.progress = Progress(
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        )
        self.task = self.progress.add_task("timer", total=self.pomo.get_state_length(self.pomo.state) * 3)

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True, padding=1)
        grid.add_column(justify="center", ratio=1)

        grid.add_row("")

        grid.add_row(
            f"{self.pomo.name()} [bold green]{timedelta(seconds=self.pomo.time_left)}[/bold green]",
        )
        grid.add_row(self.progress)
        return Panel(grid, title=":stopwatch: [bold red]Timer[/bold red]")

    def update(self):
        self.progress.update(self.task, advance=1)

    def reset(self):
        self.progress.update(self.task, total=self.pomo.get_state_length(self.pomo.state) * 60)
        self.progress.reset(self.task)


class Goals:
    """Display goals."""

    def __init__(self, pomo, goal):
        self.pomo = pomo
        self.goal = goal

    def __rich__(self) -> Panel:
        goal = self.goal
        pomo = self.pomo

        focus_time = goal * pomo.long_break_interval * pomo.pomodoro
        break_time = (goal - 1) * pomo.long_break + \
                     goal * (pomo.long_break_interval - 1) * pomo.short_break  # Short breaks
        duration = focus_time + break_time

        grid = Table.grid(expand=True, padding=1)
        grid.add_column(justify="right", ratio=1, no_wrap=True, style="green")
        grid.add_column(justify="left", ratio=1)

        grid.add_row("", "")
        grid.add_row(
            f"Goal",
            f"{self.pomo.pomodoro_count // self.pomo.long_break_interval}/{goal}"
        )

        grid.add_row(
            f"Pomos",
            f"{self.pomo.pomodoro_count}/{goal * pomo.long_break_interval}"
        )
        grid.add_row(
            f"Focus time",
            f"{timedelta(seconds=focus_time * 60)}"
        )

        grid.add_row(
            f"Break time",
            f"{timedelta(seconds=break_time * 60)}"
        )

        grid.add_row(
            f"Duration",
            f"{timedelta(seconds=duration * 60)}"
        )
        return Panel(grid, title=":dart: [bold red]Goals[/bold red]")


class Log:
    """Display log."""

    def __init__(self, pomo):
        self.pomo = pomo
        self.text = "[green]First Pomodoro![/green] Time to focus! :brain:"

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True, padding=1)
        grid.add_column(justify="center", ratio=1)
        grid.add_row("")
        grid.add_row(
            f"{self.text}"
        )
        return Panel(grid, title=":scroll: [bold red]Log[/bold red]")


def make_layout() -> Layout:
    """Define the layout."""
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
    )
    layout["main"].split_row(
        Layout(name="goals"),
        Layout(name="timer"),
        Layout(name="log"),
    )

    return layout
