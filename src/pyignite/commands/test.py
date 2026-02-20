import typer

from pyignite.commands._common import build_adapters_or_exit, run_tool_or_exit
from pyignite.tooling import ToolKey


def test_command(ctx: typer.Context) -> None:
    """Run project tests."""

    adapters = build_adapters_or_exit()
    args = tuple(ctx.args)
    run_tool_or_exit(adapters, ToolKey.TESTING, args=args, label="test")
