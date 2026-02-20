from pathlib import Path
from typing import Sequence

import typer

from pyignite.config import ConfigError, PyIgniteConfig, load_config
from pyignite.tooling import CommandResult, ToolAdapters, ToolError, ToolKey


def load_config_or_exit() -> PyIgniteConfig:
    try:
        return load_config(Path.cwd())
    except ConfigError as exc:
        typer.secho(f"ERROR [config] {exc.message}", fg=typer.colors.RED, err=True)
        typer.secho(f"Hint: {exc.hint}", fg=typer.colors.YELLOW, err=True)
        raise typer.Exit(code=2) from exc


def build_adapters_or_exit() -> ToolAdapters:
    config = load_config_or_exit()
    return ToolAdapters(config=config)


def ensure_tool_available_or_exit(adapters: ToolAdapters, key: ToolKey) -> None:
    try:
        adapters.ensure_available(key)
    except ToolError as exc:
        typer.secho(f"ERROR [tooling] {exc.message}", fg=typer.colors.RED, err=True)
        typer.secho(f"Hint: {exc.hint}", fg=typer.colors.YELLOW, err=True)
        raise typer.Exit(code=1) from exc


def run_tool_or_exit(
    adapters: ToolAdapters,
    key: ToolKey,
    *,
    args: Sequence[str] = (),
    label: str,
) -> CommandResult:
    try:
        result = adapters.run(key=key, args=args)
    except ToolError as exc:
        typer.secho(f"ERROR [tooling] {exc.message}", fg=typer.colors.RED, err=True)
        typer.secho(f"Hint: {exc.hint}", fg=typer.colors.YELLOW, err=True)
        raise typer.Exit(code=1) from exc

    if result.stdout:
        typer.echo(result.stdout, nl=False)
    if result.stderr:
        typer.echo(result.stderr, err=True, nl=False)

    if result.exit_code == 0:
        typer.secho(f"OK [{label}]", fg=typer.colors.GREEN)
        return result

    typer.secho(
        f"FAILED [{label}] exit code {result.exit_code}",
        fg=typer.colors.RED,
        err=True,
    )
    raise typer.Exit(code=result.exit_code)
