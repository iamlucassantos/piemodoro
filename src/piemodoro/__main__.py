"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """PieModoro."""


if __name__ == "__main__":
    main(prog_name="piemodoro")  # pragma: no cover
