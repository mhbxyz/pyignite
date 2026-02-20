import typer

from pyignite.commands._common import build_adapters_or_exit, ensure_tool_available_or_exit
from pyignite.tooling import ToolKey


def check_command() -> None:
    """Run all quality checks."""

    adapters = build_adapters_or_exit()
    ensure_tool_available_or_exit(adapters, ToolKey.LINTING)
    ensure_tool_available_or_exit(adapters, ToolKey.TYPING)
    ensure_tool_available_or_exit(adapters, ToolKey.TESTING)
    typer.secho("`pyignite check` is a stub for now.", fg=typer.colors.YELLOW)
