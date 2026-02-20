from __future__ import annotations

from pathlib import Path
import subprocess
import time
from typing import Callable, Iterable, Sequence

from watchfiles import watch

from pyignite.devloop.incremental import resolve_check_plan
from pyignite.devloop.renderer import CycleSummary, DevLoopRenderer
from pyignite.tooling import ToolAdapters, ToolError, ToolKey

IGNORED_PARTS = {"__pycache__", ".pytest_cache", ".ruff_cache", ".pyright", ".venv", ".git"}
IGNORED_SUFFIXES = {".pyc", ".pyo", ".swp", ".tmp"}


def run_dev_loop(
    adapters: ToolAdapters,
    *,
    watch_factory: Callable[..., Iterable[set[tuple[object, str]]]] = watch,
    popen_factory: Callable[..., subprocess.Popen[bytes]] = subprocess.Popen,
    renderer: DevLoopRenderer | None = None,
) -> None:
    config = adapters.config
    renderer = renderer or DevLoopRenderer()

    watch_paths = [config.root_dir / relative_path for relative_path in config.dev.watch]
    running_args = (
        config.run.app,
        "--host",
        config.run.host,
        "--port",
        str(config.run.port),
    )
    running_command = adapters.command(ToolKey.RUNNING, args=running_args)

    renderer.loop_started(config.dev.watch, config.dev.debounce_ms)
    server_process = _start_server(
        command=running_command,
        cwd=config.root_dir,
        popen_factory=popen_factory,
        renderer=renderer,
    )

    cycle_index = 0
    try:
        for changes in watch_factory(*watch_paths, debounce=config.dev.debounce_ms):
            changed_files = _filter_relevant_paths(changes=changes, root_dir=config.root_dir)
            if not changed_files:
                continue

            cycle_index += 1
            renderer.cycle_started(cycle_index, changed_files)
            started = time.perf_counter()

            _stop_process(server_process)
            server_process = _start_server(
                command=running_command,
                cwd=config.root_dir,
                popen_factory=popen_factory,
                renderer=renderer,
            )

            feedback = _run_feedback_checks(
                adapters, changed_files=changed_files, renderer=renderer
            )
            renderer.cycle_summary(
                CycleSummary(
                    cycle=cycle_index,
                    changed_files=tuple(changed_files),
                    plan_mode=feedback["plan_mode"],
                    plan_reason=feedback["plan_reason"],
                    steps_run=tuple(feedback["steps_run"]),
                    failed_step=feedback["failed_step"],
                    duration_ms=int((time.perf_counter() - started) * 1000),
                )
            )
    except KeyboardInterrupt:
        renderer.loop_stopped()
    finally:
        _stop_process(server_process)


def _start_server(
    *,
    command: Sequence[str],
    cwd: Path,
    popen_factory: Callable[..., subprocess.Popen[bytes]],
    renderer: DevLoopRenderer,
) -> subprocess.Popen[bytes]:
    process = popen_factory(list(command), cwd=cwd)
    renderer.server_started(command)
    return process


def _stop_process(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is not None:
        return

    process.terminate()
    try:
        process.wait(timeout=3)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=3)


def _run_feedback_checks(
    adapters: ToolAdapters,
    *,
    changed_files: Sequence[str],
    renderer: DevLoopRenderer,
) -> dict[str, object]:
    plan = resolve_check_plan(
        changed_files,
        checks_mode=adapters.config.dev.checks_mode,
        fallback_threshold=adapters.config.dev.fallback_threshold,
    )
    renderer.checks_plan(plan.mode, plan.reason, [step.name for step in plan.steps])

    summary: dict[str, object] = {
        "plan_mode": plan.mode,
        "plan_reason": plan.reason,
        "steps_run": [],
        "failed_step": None,
    }

    if not plan.steps:
        return summary

    for step in plan.steps:
        renderer.step_started(step.name)
        started = time.perf_counter()
        try:
            result = adapters.run(step.key, args=step.args)
        except ToolError as exc:
            renderer.tool_error(exc.message, exc.hint)
            summary["steps_run"].append(step.name)
            summary["failed_step"] = step.name
            return summary

        duration_ms = int((time.perf_counter() - started) * 1000)
        summary["steps_run"].append(step.name)

        if result.exit_code == 0:
            renderer.step_ok(step.name, duration_ms)
            continue

        renderer.step_failed(
            step.name,
            result.exit_code,
            duration_ms,
            _build_output_excerpt(result.stdout, result.stderr),
        )
        summary["failed_step"] = step.name
        if adapters.config.checks.stop_on_first_failure:
            return summary

    return summary


def _build_output_excerpt(stdout: str, stderr: str, *, max_lines: int = 8) -> tuple[str, ...]:
    source = stderr.strip() or stdout.strip()
    if not source:
        return ()
    lines = [line for line in source.splitlines() if line.strip()]
    return tuple(lines[:max_lines])


def _filter_relevant_paths(*, changes: set[tuple[object, str]], root_dir: Path) -> list[str]:
    selected: set[str] = set()
    for _, raw_path in changes:
        path = Path(raw_path)
        if any(part in IGNORED_PARTS for part in path.parts):
            continue
        if path.suffix in IGNORED_SUFFIXES:
            continue

        try:
            selected.add(str(path.relative_to(root_dir)))
        except ValueError:
            selected.add(str(path))

    return sorted(selected)
