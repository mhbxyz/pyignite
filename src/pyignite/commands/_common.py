from pathlib import Path

import typer

from pyignite.config import ConfigError, PyIgniteConfig, load_config


def load_config_or_exit() -> PyIgniteConfig:
    try:
        return load_config(Path.cwd())
    except ConfigError as exc:
        typer.secho(f"ERROR [config] {exc.message}", fg=typer.colors.RED, err=True)
        typer.secho(f"Hint: {exc.hint}", fg=typer.colors.YELLOW, err=True)
        raise typer.Exit(code=2) from exc
