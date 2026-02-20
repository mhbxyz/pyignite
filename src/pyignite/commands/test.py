import typer

from pyignite.commands._common import build_adapters_or_exit, ensure_tool_available_or_exit
from pyignite.tooling import ToolKey


def test_command() -> None:
    """Run project tests."""

    adapters = build_adapters_or_exit()
    ensure_tool_available_or_exit(adapters, ToolKey.TESTING)
    typer.secho("`pyignite test` is a stub for now.", fg=typer.colors.YELLOW)
