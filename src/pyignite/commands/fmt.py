import typer

from pyignite.commands._common import build_adapters_or_exit, ensure_tool_available_or_exit
from pyignite.tooling import ToolKey


def fmt_command() -> None:
    """Run code formatting."""

    adapters = build_adapters_or_exit()
    ensure_tool_available_or_exit(adapters, ToolKey.LINTING)
    typer.secho("`pyignite fmt` is a stub for now.", fg=typer.colors.YELLOW)
