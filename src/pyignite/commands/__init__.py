import typer

from pyignite.commands import check, dev, fmt, lint, run, test


def register_commands(app: typer.Typer) -> None:
    """Register all command groups on the root app."""

    app.command(name="dev")(dev.dev_command)
    app.command(name="run")(run.run_command)
    app.command(name="test")(test.test_command)
    app.command(name="lint")(lint.lint_command)
    app.command(name="fmt")(fmt.fmt_command)
    app.command(name="check")(check.check_command)
