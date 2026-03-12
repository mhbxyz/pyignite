from pathlib import Path
import subprocess
from typing import Sequence

import pytest

from flint.config import (
    ChecksSection,
    DevSection,
    ProjectSection,
    FlintConfig,
    RunSection,
    ToolingSection,
)
from flint.tooling.adapters import SubprocessRunner
from flint.tooling import ToolAdapters, ToolKey, ToolNotAvailableError


class FakeRunner(SubprocessRunner):
    def __init__(self, return_code: int, stdout: str = "", stderr: str = "") -> None:
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr
        self.last_command: tuple[str, ...] | None = None
        self.last_cwd: Path | None = None
        self.last_capture_output: bool | None = None

    def run(
        self,
        command: Sequence[str],
        cwd: Path,
        *,
        capture_output: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        self.last_command = tuple(command)
        self.last_cwd = cwd
        self.last_capture_output = capture_output
        return subprocess.CompletedProcess(
            args=list(command),
            returncode=self.return_code,
            stdout=self.stdout,
            stderr=self.stderr,
        )


def _config(tmp_path: Path) -> FlintConfig:
    return FlintConfig(
        root_dir=tmp_path,
        file_path=tmp_path / "flint.toml",
        project=ProjectSection(),
        tooling=ToolingSection(),
        dev=DevSection(),
        run=RunSection(),
        checks=ChecksSection(),
    )


def test_missing_tool_raises_actionable_error(tmp_path: Path) -> None:
    adapters = ToolAdapters(config=_config(tmp_path), which=lambda _: None)

    with pytest.raises(ToolNotAvailableError, match="Configured runner") as exc_info:
        adapters.ensure_available(ToolKey.LINTING)

    assert "[tooling].runner" in exc_info.value.hint
    assert "uv sync --extra dev" in exc_info.value.hint


def test_run_propagates_subprocess_exit_and_output(tmp_path: Path) -> None:
    runner = FakeRunner(return_code=7, stdout="out", stderr="err")
    adapters = ToolAdapters(
        config=_config(tmp_path),
        runner=runner,
        which=lambda _: "/usr/bin/tool",
    )

    result = adapters.run(ToolKey.TESTING, args=("-q",))

    assert result.command == ("uv", "run", "pytest", "-q")
    assert result.exit_code == 7
    assert result.stdout == "out"
    assert result.stderr == "err"
    assert runner.last_command == ("uv", "run", "pytest", "-q")
    assert runner.last_cwd == tmp_path
    assert runner.last_capture_output is True


def test_run_with_live_output_disables_capture(tmp_path: Path) -> None:
    runner = FakeRunner(return_code=0)
    adapters = ToolAdapters(
        config=_config(tmp_path),
        runner=runner,
        which=lambda _: "/usr/bin/tool",
    )

    result = adapters.run(ToolKey.RUNNING, args=("myapi.main:app",), live_output=True)

    assert result.command == ("uv", "run", "uvicorn", "myapi.main:app")
    assert result.exit_code == 0
    assert runner.last_capture_output is False


def test_tooling_config_controls_executable_name(tmp_path: Path) -> None:
    config = _config(tmp_path)
    config = FlintConfig(
        root_dir=config.root_dir,
        file_path=config.file_path,
        project=config.project,
        tooling=ToolingSection(runner="my-uv", linting="my-ruff", testing="my-pytest"),
        dev=config.dev,
        run=config.run,
        checks=config.checks,
    )
    runner = FakeRunner(return_code=0)
    adapters = ToolAdapters(config=config, runner=runner, which=lambda _: "/usr/bin/tool")

    lint_result = adapters.run(ToolKey.LINTING, args=("check", "."))
    test_result = adapters.run(ToolKey.TESTING)

    assert lint_result.command == ("my-uv", "run", "my-ruff", "check", ".")
    assert test_result.command == ("my-uv", "run", "my-pytest")
