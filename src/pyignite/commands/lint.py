import typer

from pyignite.commands._common import build_adapters_or_exit, ensure_tool_available_or_exit
from pyignite.tooling import ToolKey


def lint_command() -> None:
    """Run lint checks."""

    adapters = build_adapters_or_exit()
    ensure_tool_available_or_exit(adapters, ToolKey.LINTING)
    typer.secho("`pyignite lint` is a stub for now.", fg=typer.colors.YELLOW)
