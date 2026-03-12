from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
import shutil
import subprocess
from typing import Callable, Sequence

from flint.config import FlintConfig


class ToolKey(StrEnum):
    LINTING = "linting"
    TESTING = "testing"
    TYPING = "typing"
    RUNNING = "running"


class ToolError(Exception):
    def __init__(self, message: str, hint: str) -> None:
        super().__init__(message)
        self.message = message
        self.hint = hint


class ToolNotAvailableError(ToolError):
    """Raised when a configured executable cannot be found."""


@dataclass(slots=True, frozen=True)
class CommandResult:
    command: tuple[str, ...]
    exit_code: int
    stdout: str
    stderr: str


@dataclass(slots=True, frozen=True)
class ToolSpec:
    key: ToolKey
    executable: str
    remediation_hint: str


class SubprocessRunner:
    def run(
        self,
        command: Sequence[str],
        cwd: Path,
        *,
        capture_output: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            list(command),
            cwd=cwd,
            check=False,
            capture_output=capture_output,
            text=True,
        )


class ToolAdapters:
    def __init__(
        self,
        config: FlintConfig,
        runner: SubprocessRunner | None = None,
        which: Callable[[str], str | None] | None = None,
    ) -> None:
        self._config = config
        self._runner = runner or SubprocessRunner()
        self._which = which or shutil.which

    @property
    def config(self) -> FlintConfig:
        return self._config

    def spec(self, key: ToolKey) -> ToolSpec:
        executable = {
            ToolKey.LINTING: self._config.tooling.linting,
            ToolKey.TESTING: self._config.tooling.testing,
            ToolKey.TYPING: self._config.tooling.typing,
            ToolKey.RUNNING: self._config.tooling.running,
        }[key]

        return ToolSpec(
            key=key,
            executable=executable,
            remediation_hint=(
                f"Install `{executable}` and retry, or set `[tooling].{key.value}` "
                "to a valid executable."
            ),
        )

    def ensure_available(self, key: ToolKey) -> ToolSpec:
        spec = self.spec(key)
        runner_executable = self._config.tooling.runner
        if self._which(runner_executable):
            return spec
        raise ToolNotAvailableError(
            f"Configured runner for `{key.value}` not found: `{runner_executable}`.",
            self._missing_runner_hint(runner_executable),
        )

    def run(
        self,
        key: ToolKey,
        args: Sequence[str] = (),
        cwd: Path | None = None,
        *,
        live_output: bool = False,
    ) -> CommandResult:
        command = self.command(key=key, args=args)
        completed = self._runner.run(
            command=command,
            cwd=cwd or self._config.root_dir,
            capture_output=not live_output,
        )

        return CommandResult(
            command=tuple(command),
            exit_code=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )

    def command(self, key: ToolKey, args: Sequence[str] = ()) -> tuple[str, ...]:
        spec = self.ensure_available(key)
        return (self._config.tooling.runner, "run", spec.executable, *args)

    def _missing_runner_hint(self, runner_executable: str) -> str:
        if runner_executable == "uv":
            return (
                "Install `uv`, prepare the project with `uv sync --extra dev`, "
                "and retry, or set `[tooling].runner` to a valid executable."
            )
        return (
            f"Install `{runner_executable}` and retry, or set `[tooling].runner` "
            "to a valid executable."
        )
