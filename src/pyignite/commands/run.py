import typer

from pyignite.commands._common import load_config_or_exit


def run_command() -> None:
    """Run the application in non-watch mode."""

    _ = load_config_or_exit()
    typer.secho("`pyignite run` is a stub for now.", fg=typer.colors.YELLOW)
