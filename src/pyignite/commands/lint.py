import typer

from pyignite.commands._common import load_config_or_exit


def lint_command() -> None:
    """Run lint checks."""

    _ = load_config_or_exit()
    typer.secho("`pyignite lint` is a stub for now.", fg=typer.colors.YELLOW)
