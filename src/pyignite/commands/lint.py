import typer

from pyignite.commands._common import build_adapters_or_exit, run_tool_or_exit
from pyignite.tooling import ToolKey


def lint_command(ctx: typer.Context) -> None:
    """Run lint checks."""

    adapters = build_adapters_or_exit()
    args = tuple(ctx.args) if ctx.args else ("check", ".")
    run_tool_or_exit(adapters, ToolKey.LINTING, args=args, label="lint")
