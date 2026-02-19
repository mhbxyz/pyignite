import typer

from pyignite.commands._common import load_config_or_exit


def fmt_command() -> None:
    """Run code formatting."""

    _ = load_config_or_exit()
    typer.secho("`pyignite fmt` is a stub for now.", fg=typer.colors.YELLOW)
