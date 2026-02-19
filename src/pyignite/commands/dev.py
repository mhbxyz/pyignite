import typer

from pyignite.commands._common import load_config_or_exit


def dev_command() -> None:
    """Run the local development loop."""

    _ = load_config_or_exit()
    typer.secho("`pyignite dev` is a stub for now.", fg=typer.colors.YELLOW)
