import typer

from pyignite.commands._common import build_adapters_or_exit, run_tool_or_exit
from pyignite.tooling import ToolKey


def run_command(ctx: typer.Context) -> None:
    """Run the application in non-watch mode."""

    adapters = build_adapters_or_exit()
    default_args = (
        adapters.config.run.app,
        "--host",
        adapters.config.run.host,
        "--port",
        str(adapters.config.run.port),
    )
    args = default_args + tuple(ctx.args)
    run_tool_or_exit(adapters, ToolKey.RUNNING, args=args, label="run")
