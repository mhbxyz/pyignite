from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from flint.cli import app
from tests.helpers import copy_fixture

runner = CliRunner()


def test_run_resolves_fastapi_src_layout_sample(tmp_path: Path) -> None:
    project = copy_fixture(tmp_path, "fastapi_sample")

    with patch("flint.tools.ensure_uv_available"), patch("flint.tools.subprocess.run") as run_mock:
        run_mock.return_value.returncode = 0
        result = runner.invoke(app, ["run", "--cwd", str(project)])

    assert result.exit_code == 0
    command = run_mock.call_args.args[0]
    assert command == ["uv", "run", "uvicorn", "demo_api.main:app", "--reload"]


def test_dev_restarts_on_source_change_and_reports_cycle(tmp_path: Path) -> None:
    project = copy_fixture(tmp_path, "fastapi_sample")
    process = MagicMock()
    process.poll.return_value = None
    process.wait.return_value = 0

    changes = [
        {(1, str(project / "src" / "demo_api" / "main.py"))},
        KeyboardInterrupt(),
    ]

    def fake_watch(*paths: Path, **kwargs: object):
        for item in changes:
            if isinstance(item, BaseException):
                raise item
            yield item

    with (
        patch("flint.devloop.spawn_background", return_value=process) as spawn_mock,
        patch("flint.devloop.watch", side_effect=fake_watch),
        patch("flint.devloop.run_check_pipeline", return_value=0) as check_mock,
    ):
        result = runner.invoke(app, ["dev", "--cwd", str(project)])

    assert result.exit_code == 0
    assert spawn_mock.call_count == 2
    assert check_mock.call_count == 2
    assert "==> dev cycle: initial" in result.stdout
    assert "Restarting server" in result.stdout
    assert "OK dev cycle: change" in result.stdout


def test_dev_reacts_to_test_change_without_restart(tmp_path: Path) -> None:
    project = copy_fixture(tmp_path, "fastapi_sample")
    process = MagicMock()
    process.poll.return_value = None
    process.wait.return_value = 0

    changes = [
        {(1, str(project / "tests" / "test_health.py"))},
        KeyboardInterrupt(),
    ]

    def fake_watch(*paths: Path, **kwargs: object):
        for item in changes:
            if isinstance(item, BaseException):
                raise item
            yield item

    with (
        patch("flint.devloop.spawn_background", return_value=process) as spawn_mock,
        patch("flint.devloop.watch", side_effect=fake_watch),
        patch("flint.devloop.run_check_pipeline", return_value=0) as check_mock,
    ):
        result = runner.invoke(app, ["dev", "--cwd", str(project)])

    assert result.exit_code == 0
    assert spawn_mock.call_count == 1
    assert check_mock.call_count == 2
    assert "==> dev cycle: change" in result.stdout


def test_check_fails_fast_when_tool_is_missing(tmp_path: Path) -> None:
    project = copy_fixture(tmp_path, "fastapi_sample")

    def fake_ensure(tool_name: str, cwd: Path) -> None:
        if tool_name == "ruff":
            from flint.errors import tooling_error

            raise tooling_error(
                "Required tool `ruff` is not available.",
                "Install project dev dependencies with `uv sync --extra dev` and retry.",
            )

    with patch("flint.tools.ensure_uv_available", side_effect=fake_ensure):
        result = runner.invoke(app, ["check", "--cwd", str(project)])

    assert result.exit_code == 1
    assert "ERROR [tooling] Required tool `ruff` is not available." in result.stderr
