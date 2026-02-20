from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence

import typer


@dataclass(slots=True, frozen=True)
class CycleSummary:
    cycle: int
    changed_files: tuple[str, ...]
    plan_mode: str
    plan_reason: str
    steps_run: tuple[str, ...]
    failed_step: str | None
    duration_ms: int


class DevLoopRenderer:
    def __init__(
        self,
        *,
        secho: Callable[..., None] = typer.secho,
        echo: Callable[..., None] = typer.echo,
    ) -> None:
        self._secho = secho
        self._echo = echo

    def loop_started(self, watch_paths: Sequence[str], debounce_ms: int) -> None:
        self._secho("Dev loop started", fg=typer.colors.CYAN)
        self._secho(
            f"Watching {', '.join(watch_paths)} (debounce {debounce_ms}ms)",
            fg=typer.colors.CYAN,
        )

    def loop_stopped(self) -> None:
        self._secho("Dev loop stopped", fg=typer.colors.YELLOW)

    def server_started(self, command: Sequence[str]) -> None:
        self._secho(f"Server up: {' '.join(command)}", fg=typer.colors.GREEN)

    def cycle_started(self, cycle: int, changed_files: Sequence[str]) -> None:
        self._secho(
            f"Cycle #{cycle}: {len(changed_files)} change(s): {', '.join(changed_files[:3])}",
            fg=typer.colors.CYAN,
        )
        if len(changed_files) > 3:
            self._secho(f"... +{len(changed_files) - 3} more file(s)", fg=typer.colors.CYAN)

    def checks_plan(self, mode: str, reason: str, steps: Sequence[str]) -> None:
        if not steps:
            self._secho(f"Checks: {mode} ({reason}) -> none", fg=typer.colors.BLUE)
            return
        self._secho(
            f"Checks: {mode} ({reason}) -> {' -> '.join(steps)}",
            fg=typer.colors.BLUE,
        )

    def step_started(self, step: str) -> None:
        self._secho(f"Run [{step}]", fg=typer.colors.CYAN)

    def step_ok(self, step: str, duration_ms: int) -> None:
        self._secho(f"OK [{step}] {duration_ms}ms", fg=typer.colors.GREEN)

    def step_failed(
        self, step: str, exit_code: int, duration_ms: int, excerpt: Sequence[str]
    ) -> None:
        self._secho(
            f"FAILED [{step}] exit {exit_code} ({duration_ms}ms)", fg=typer.colors.RED, err=True
        )
        if excerpt:
            self._secho("Details:", fg=typer.colors.RED, err=True)
            for line in excerpt:
                self._echo(line, err=True)
        self._secho(
            f"Hint: run `pyignite {step}` for full output.",
            fg=typer.colors.YELLOW,
            err=True,
        )

    def tool_error(self, message: str, hint: str) -> None:
        self._secho(f"ERROR [tooling] {message}", fg=typer.colors.RED, err=True)
        self._secho(f"Hint: {hint}", fg=typer.colors.YELLOW, err=True)

    def cycle_summary(self, summary: CycleSummary) -> None:
        if summary.failed_step:
            self._secho(
                f"Summary #{summary.cycle}: failed on {summary.failed_step} after {summary.duration_ms}ms",
                fg=typer.colors.RED,
                err=True,
            )
            return

        self._secho(
            f"Summary #{summary.cycle}: passed ({', '.join(summary.steps_run)}) in {summary.duration_ms}ms",
            fg=typer.colors.GREEN,
        )
