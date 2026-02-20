import typer

from pyignite.commands._common import build_adapters_or_exit, ensure_tool_available_or_exit
from pyignite.tooling import ToolKey


def run_command() -> None:
    """Run the application in non-watch mode."""

    adapters = build_adapters_or_exit()
    ensure_tool_available_or_exit(adapters, ToolKey.RUNNING)
    typer.secho("`pyignite run` is a stub for now.", fg=typer.colors.YELLOW)
