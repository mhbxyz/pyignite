import typer

from pyignite.commands._common import load_config_or_exit


def check_command() -> None:
    """Run all quality checks."""

    _ = load_config_or_exit()
    typer.secho("`pyignite check` is a stub for now.", fg=typer.colors.YELLOW)
