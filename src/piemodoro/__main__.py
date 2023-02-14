"""Command-line interface."""
import typer
import shutil
import yaml
from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm
from rich.panel import Panel
from rich.progress import Progress, RenderableColumn
from rich.markdown import Markdown
import datetime
import pygame.mixer as mixer
from .config import Configuration
from .pomodoro import Pomo
from typing import Optional

# Create typer app
app = typer.Typer(no_args_is_help=True)

# Set constant variables
APP_NAME = "piemodoro"
CONFIG_DIR = Path(typer.get_app_dir(APP_NAME))
SRC_DIR = Path(__file__).parent
DEFAULT_CONFIG_FILE = SRC_DIR / "config.yaml"
USER_CONFIG = CONFIG_DIR / "user_config.yaml"

# Set console
console = Console()


@app.command()
def start(goal: Optional[int] = typer.Argument(None, help="Number of pomodoro sets to run."),
          ask: Optional[bool] = typer.Option(False, help="Ask to continue after timer is finished."),
          mute: Optional[bool] = typer.Option(False, help="Mute the timer sound."),):
    """Start a new pomodoro session."""
    config_file = USER_CONFIG if USER_CONFIG.exists() else DEFAULT_CONFIG_FILE
    with open(config_file, "r") as f:
        config_data = Configuration(**yaml.load(f, Loader=yaml.SafeLoader))

    pomo = Pomo(**config_data.dict())

    start_str = f"""
[bold bright_green]Starting the pomodoro session![/bold bright_green]
[magenta]Goal: [/magenta]{goal if goal is not None else 'unlimited'} pomodoro sets
"""

    if goal is not None:
        focus_time = goal * pomo.long_break_interval * pomo.pomodoro
        break_time = (goal - 1) * pomo.long_break + \
                     goal * (pomo.long_break_interval - 1) * pomo.short_break  # Short breaks
        duration = focus_time + break_time

        start_str += f"""[magenta]Pomodoros[/magenta]: {goal * pomo.long_break_interval} ({pomo.pomodoro} minutes each)
[magenta]Focus time[/magenta]: {datetime.timedelta(seconds=focus_time * 60)}
[magenta]Break time[/magenta]: {datetime.timedelta(seconds=break_time * 60)}
[magenta]Duration[/magenta]: {datetime.timedelta(seconds=duration * 60)}
"""

    console.print(Panel.fit(start_str, title=":pie: [bold red]PieModoro[/bold red] :tomato:",
                            subtitle="[i]Time to Focus[/i]"))

    while True and (goal is None or pomo.pomodoro_count // pomo.long_break_interval < goal):
        with Progress(
                *Progress.get_default_columns(),
                RenderableColumn(pomo.emoji()),
                transient=True,
                console=console,
        ) as progress:
            task = progress.add_task(f"{pomo.name()}", total=pomo.time_left)

            while pomo.time_left > 0:
                pomo.tick()
                progress.update(task, advance=1)

        # console.log(f"Finished {pomo.name()}: {pomo.emoji()}")

        if pomo.state == "pomodoro":

            console.log(f"[bold green]{pomo.name()} finished![/bold green] Time to take a break. :coffee:")
            tune = "pomo.mp3"
        else:
            console.log(f"[bold blue]{pomo.name()} finished![/bold blue] Time to get back to work. :hammer:")
            tune = "break.mp3"

        if not mute:
            mixer.init()
            mixer.music.load(SRC_DIR / tune)
            mixer.music.play()

        if ask:
            if not Confirm.ask("Do you want to continue?", default=True):
                typer.Exit()

        # Move to next timer state
        pomo.switch()

    console.print("Session finished! :tada:")


@app.command()
def config(
        reset: bool = typer.Option(default=False, help="Reset the user configuration to the default values")) -> None:
    """Configure PieModoro."""

    if not CONFIG_DIR.exists():
        if Confirm.ask("No config file found. Would you like to create one? [y/n] "):
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            shutil.copy(DEFAULT_CONFIG_FILE, USER_CONFIG)
            console.print(f"Config file created at '{USER_CONFIG}' :smiley:")

    else:
        if reset:
            if Confirm.ask("Are you sure you want to reset your configuration? [y/n] "):
                console.print(f"Config file reset to default at '{USER_CONFIG}' :smiley:")
            else:
                console.print(f"Your config file is located at '{USER_CONFIG}' :smiley:")

    if __name__ == "__main__":
        typer.run(main)  # pragma: no cover
