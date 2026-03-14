from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
from typing import Iterable

from watchfiles import Change, watch

from flint.config import ProjectSettings
from flint.errors import tooling_error
from flint.tools import build_run_command, run_check_pipeline, spawn_background


@dataclass(slots=True)
class ChangeDecision:
    restart_server: bool
    run_checks: bool


def classify_changes(root: Path, changed_paths: Iterable[str]) -> ChangeDecision:
    root = root.resolve()
    restart_server = False
    run_checks = False

    for raw_path in changed_paths:
        path = Path(raw_path).resolve()
        try:
            relative = path.relative_to(root)
        except ValueError:
            continue

        top = relative.parts[0] if relative.parts else ""
        if top == "src" or relative.name in {"flint.toml", "pyproject.toml"}:
            restart_server = True
            run_checks = True
        elif top == "tests":
            run_checks = True

    return ChangeDecision(restart_server=restart_server, run_checks=run_checks)


def run_dev_loop(settings: ProjectSettings) -> int:
    server = ServerProcess(settings)
    print("==> dev cycle: initial")
    server.start()
    check_exit_code = run_check_pipeline(settings)
    if check_exit_code != 0:
        print("FAILED dev cycle: initial")
    else:
        print("OK dev cycle: initial")

    try:
        for changes in watch(*settings.watch_paths, raise_interrupt=False):
            changed_paths = [path for _, path in changes]
            decision = classify_changes(settings.root, changed_paths)
            if not decision.restart_server and not decision.run_checks:
                continue
            print("==> dev cycle: change")
            if decision.restart_server:
                print("Restarting server")
                server.restart()
            if decision.run_checks:
                check_exit_code = run_check_pipeline(settings)
                if check_exit_code != 0:
                    print("FAILED dev cycle: change")
                else:
                    print("OK dev cycle: change")
    except KeyboardInterrupt:
        return 0
    except OSError as exc:
        raise tooling_error(
            "The file watcher failed.",
            "Check that the configured watch paths exist and are readable.",
        ) from exc
    finally:
        server.stop()
    return 0


class ServerProcess:
    def __init__(self, settings: ProjectSettings) -> None:
        self._settings = settings
        self._process: subprocess.Popen[str] | None = None

    def start(self) -> None:
        if self._process is not None:
            return
        self._process = spawn_background(
            build_run_command(self._settings, reload_enabled=False),
            self._settings.root,
        )
        if self._process.poll() is not None:
            raise tooling_error(
                "The ASGI server exited immediately.",
                "Run `flint run` to inspect the startup failure directly.",
            )

    def restart(self) -> None:
        self.stop()
        self.start()

    def stop(self) -> None:
        if self._process is None:
            return
        if self._process.poll() is None:
            self._process.terminate()
            try:
                self._process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._process.kill()
                self._process.wait(timeout=5)
        self._process = None
