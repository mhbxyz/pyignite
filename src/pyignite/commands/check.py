import typer

from pyignite.commands._common import build_adapters_or_exit
from pyignite.tooling import ToolError, ToolKey


def check_command() -> None:
    """Run all quality checks."""

    adapters = build_adapters_or_exit()
    failures: list[tuple[str, int]] = []

    step_map: dict[str, tuple[ToolKey, tuple[str, ...]]] = {
        "lint": (ToolKey.LINTING, ("check", ".")),
        "type": (ToolKey.TYPING, ()),
        "test": (ToolKey.TESTING, ()),
    }

    for step in adapters.config.checks.pipeline:
        tool_key, args = step_map[step]
        typer.secho(f"Running [{step}]...", fg=typer.colors.CYAN)
        try:
            result = adapters.run(tool_key, args=args)
        except ToolError as exc:
            typer.secho(f"ERROR [tooling] {exc.message}", fg=typer.colors.RED, err=True)
            typer.secho(f"Hint: {exc.hint}", fg=typer.colors.YELLOW, err=True)
            raise typer.Exit(code=1) from exc

        if result.stdout:
            typer.echo(result.stdout, nl=False)
        if result.stderr:
            typer.echo(result.stderr, err=True, nl=False)

        if result.exit_code == 0:
            typer.secho(f"OK [{step}]", fg=typer.colors.GREEN)
            continue

        typer.secho(f"FAILED [{step}] exit code {result.exit_code}", fg=typer.colors.RED, err=True)
        failures.append((step, result.exit_code))
        if adapters.config.checks.stop_on_first_failure:
            break

    if not failures:
        typer.secho("CHECK SUMMARY: all steps passed", fg=typer.colors.GREEN)
        return

    failed_steps = ", ".join(step for step, _ in failures)
    typer.secho(
        f"CHECK SUMMARY: failed step(s): {failed_steps}",
        fg=typer.colors.RED,
        err=True,
    )
    raise typer.Exit(code=failures[0][1])
