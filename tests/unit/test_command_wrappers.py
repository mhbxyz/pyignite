from collections import deque
from dataclasses import dataclass, field
from types import SimpleNamespace

from typer.testing import CliRunner

from pyignite.cli import app
from pyignite.tooling import CommandResult, ToolKey


@dataclass(slots=True)
class FakeAdapters:
    config: object
    responses: deque[CommandResult]
    calls: list[tuple[ToolKey, tuple[str, ...]]] = field(default_factory=list)

    def run(self, key: ToolKey, args: tuple[str, ...] = (), cwd: None = None) -> CommandResult:
        _ = cwd
        self.calls.append((key, tuple(args)))
        return self.responses.popleft()


def _config(*, stop_on_first_failure: bool = True) -> object:
    return SimpleNamespace(
        run=SimpleNamespace(app="app.main:app", host="127.0.0.1", port=8000),
        checks=SimpleNamespace(
            pipeline=("lint", "type", "test"),
            stop_on_first_failure=stop_on_first_failure,
        ),
    )


def _result(exit_code: int, stdout: str = "", stderr: str = "") -> CommandResult:
    return CommandResult(command=("tool",), exit_code=exit_code, stdout=stdout, stderr=stderr)


def test_lint_runs_default_args(monkeypatch) -> None:
    from pyignite.commands import lint

    adapters = FakeAdapters(config=_config(), responses=deque([_result(0)]))
    monkeypatch.setattr(lint, "build_adapters_or_exit", lambda: adapters)

    result = CliRunner().invoke(app, ["lint"])

    assert result.exit_code == 0
    assert adapters.calls == [(ToolKey.LINTING, ("check", "."))]
    assert "OK [lint]" in result.stdout


def test_lint_propagates_tool_exit_code(monkeypatch) -> None:
    from pyignite.commands import lint

    adapters = FakeAdapters(config=_config(), responses=deque([_result(7)]))
    monkeypatch.setattr(lint, "build_adapters_or_exit", lambda: adapters)

    result = CliRunner().invoke(app, ["lint"])

    assert result.exit_code == 7
    assert "FAILED [lint] exit code 7" in result.output


def test_run_uses_defaults_and_passthrough_args(monkeypatch) -> None:
    from pyignite.commands import run

    adapters = FakeAdapters(config=_config(), responses=deque([_result(0)]))
    monkeypatch.setattr(run, "build_adapters_or_exit", lambda: adapters)

    result = CliRunner().invoke(app, ["run", "--reload"])

    assert result.exit_code == 0
    assert adapters.calls == [
        (
            ToolKey.RUNNING,
            ("app.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"),
        )
    ]


def test_check_runs_full_pipeline_and_reports_summary(monkeypatch) -> None:
    from pyignite.commands import check

    adapters = FakeAdapters(
        config=_config(stop_on_first_failure=False),
        responses=deque([_result(0), _result(3), _result(0)]),
    )
    monkeypatch.setattr(check, "build_adapters_or_exit", lambda: adapters)

    result = CliRunner().invoke(app, ["check"])

    assert result.exit_code == 3
    assert adapters.calls == [
        (ToolKey.LINTING, ("check", ".")),
        (ToolKey.TYPING, ()),
        (ToolKey.TESTING, ()),
    ]
    assert "CHECK SUMMARY: failed step(s): type" in result.output
