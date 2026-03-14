from pathlib import Path
import io
from unittest.mock import patch

import pytest

from flint.config import ProjectSettings
from flint.errors import FlintError
from flint.tools import build_run_command, run_check_pipeline


def make_settings(tmp_path: Path, typecheck: bool = False) -> ProjectSettings:
    return ProjectSettings(
        root=tmp_path,
        app_module="demo.main:app",
        watch_paths=[tmp_path / "src"],
        typecheck=typecheck,
    )


def test_build_run_command_uses_uvicorn_reload(tmp_path: Path) -> None:
    settings = make_settings(tmp_path)

    assert build_run_command(settings, reload_enabled=True) == [
        "uv",
        "run",
        "uvicorn",
        "demo.main:app",
        "--reload",
    ]


def test_run_check_pipeline_runs_in_fixed_order(tmp_path: Path) -> None:
    settings = make_settings(tmp_path, typecheck=True)
    calls: list[list[str]] = []

    def fake_run(command: list[str], cwd: Path) -> int:
        calls.append(command)
        return 0

    with patch("flint.tools.run_step", side_effect=fake_run), patch("flint.tools.ensure_uv_available"):
        exit_code = run_check_pipeline(settings)

    assert exit_code == 0
    assert calls == [
        ["uv", "run", "ruff", "check", "."],
        ["uv", "run", "pytest"],
        ["uv", "run", "pyright"],
    ]


def test_run_check_pipeline_stops_on_failure(tmp_path: Path) -> None:
    settings = make_settings(tmp_path, typecheck=True)
    calls: list[list[str]] = []

    def fake_run(command: list[str], cwd: Path) -> int:
        calls.append(command)
        return 1 if command[2] == "pytest" else 0

    with patch("flint.tools.run_step", side_effect=fake_run), patch("flint.tools.ensure_uv_available"):
        exit_code = run_check_pipeline(settings)

    assert exit_code == 1
    assert calls == [
        ["uv", "run", "ruff", "check", "."],
        ["uv", "run", "pytest"],
    ]


def test_run_check_pipeline_errors_when_required_tool_is_missing(tmp_path: Path) -> None:
    settings = make_settings(tmp_path)

    def fail_on_ruff(tool_name: str, cwd: Path) -> None:
        if tool_name == "ruff":
            raise FlintError(
                message="Required tool `ruff` is not available.",
                hint="Install project dev dependencies with `uv sync --extra dev` and retry.",
                category="tooling",
                exit_code=1,
            )

    with patch("flint.tools.ensure_uv_available", side_effect=fail_on_ruff):
        with pytest.raises(FlintError) as exc_info:
            run_check_pipeline(settings)

    assert exc_info.value.category == "tooling"
    assert "Required tool `ruff` is not available." in exc_info.value.message


def test_run_check_pipeline_prints_stage_summary(tmp_path: Path) -> None:
    settings = make_settings(tmp_path)
    stream = io.StringIO()

    with patch("flint.tools.run_step", return_value=0), patch("flint.tools.ensure_uv_available"):
        exit_code = run_check_pipeline(settings, stdout=stream)

    assert exit_code == 0
    assert "==> lint" in stream.getvalue()
    assert "OK test" in stream.getvalue()
