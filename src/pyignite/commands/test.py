import typer

from pyignite.commands._common import load_config_or_exit


def test_command() -> None:
    """Run project tests."""

    _ = load_config_or_exit()
    typer.secho("`pyignite test` is a stub for now.", fg=typer.colors.YELLOW)
