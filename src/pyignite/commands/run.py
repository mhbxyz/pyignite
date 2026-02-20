import typer

from pyignite.commands._common import build_adapters_or_exit
from pyignite.tooling import ToolError, ToolKey


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

    try:
        result = adapters.run(ToolKey.RUNNING, args=args)
    except ToolError as exc:
        typer.secho(f"ERROR [tooling] {exc.message}", fg=typer.colors.RED, err=True)
        typer.secho(f"Hint: {exc.hint}", fg=typer.colors.YELLOW, err=True)
        raise typer.Exit(code=1) from exc

    if result.stdout:
        typer.echo(result.stdout, nl=False)
    if result.stderr:
        typer.echo(result.stderr, err=True, nl=False)

    if result.exit_code == 0:
        typer.secho("OK [run]", fg=typer.colors.GREEN)
        return

    typer.secho(
        f"ERROR [tooling] Failed to run ASGI app `{adapters.config.run.app}`.",
        fg=typer.colors.RED,
        err=True,
    )

    hint = _build_runtime_hint(stderr=result.stderr, app_path=adapters.config.run.app)
    if hint:
        typer.secho(f"Hint: {hint}", fg=typer.colors.YELLOW, err=True)

    raise typer.Exit(code=result.exit_code)


def _build_runtime_hint(*, stderr: str, app_path: str) -> str:
    lower_stderr = stderr.lower()
    if "error loading asgi app" in lower_stderr or "could not import module" in lower_stderr:
        return (
            "Check `[run].app` in `pyignite.toml` and ensure the module exists under `src/` "
            f"with an ASGI app at `{app_path}`."
        )
    if 'attribute "app" not found' in lower_stderr:
        return f"Expose an `app` variable in `{app_path}` or override `[run].app` accordingly."
    return "Review uvicorn output above, fix runtime errors, and retry."
