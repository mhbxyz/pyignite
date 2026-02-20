from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import json
import os
from pathlib import Path
import statistics
import subprocess
import sys
import tempfile
import time


@dataclass(slots=True, frozen=True)
class ScenarioResult:
    name: str
    samples_ms: list[float]

    def as_dict(self) -> dict[str, object]:
        p50_ms = float(statistics.median(self.samples_ms))
        p95_ms = float(_percentile(self.samples_ms, 0.95))
        return {
            "samples_ms": [round(value, 2) for value in self.samples_ms],
            "p50_ms": round(p50_ms, 2),
            "p95_ms": round(p95_ms, 2),
        }


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    output_path = repo_root / "benchmarks" / "current.alpha.json"
    if len(sys.argv) > 1 and sys.argv[1] == "--output" and len(sys.argv) > 2:
        output_path = Path(sys.argv[2]).resolve()

    with tempfile.TemporaryDirectory(prefix="pyignite-bench-") as temp_dir_raw:
        temp_dir = Path(temp_dir_raw)
        project_dir = _create_sample_project(repo_root=repo_root, workspace=temp_dir)

        startup = ScenarioResult(
            name="startup_run",
            samples_ms=[
                _measure_startup_cycle(project_dir=project_dir, repo_root=repo_root)
                for _ in range(3)
            ],
        )
        save_feedback = ScenarioResult(
            name="save_to_feedback_incremental_test_change",
            samples_ms=[
                _measure_incremental_feedback_cycle(project_dir=project_dir, repo_root=repo_root)
                for _ in range(3)
            ],
        )

    payload = {
        "metadata": {
            "generated_at": datetime.now(tz=UTC).isoformat(),
            "python": sys.version.split()[0],
            "platform": sys.platform,
            "commit": _git_head(repo_root),
        },
        "scenarios": {
            startup.name: startup.as_dict(),
            save_feedback.name: save_feedback.as_dict(),
        },
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote benchmark report: {output_path}")


def _create_sample_project(*, repo_root: Path, workspace: Path) -> Path:
    env = _bench_env(repo_root)
    _run(
        [
            sys.executable,
            "-m",
            "pyignite",
            "new",
            "sample",
            "--profile",
            "api",
            "--template",
            "fastapi",
        ],
        cwd=workspace,
        env=env,
        timeout=120,
    )

    project_dir = workspace / "sample"
    _run(["uv", "sync", "--extra", "dev"], cwd=project_dir, env=env, timeout=240)
    return project_dir


def _measure_startup_cycle(*, project_dir: Path, repo_root: Path) -> float:
    env = _bench_env(repo_root)
    port = _free_port()
    config_path = project_dir / "pyignite.toml"
    _set_run_port(config_path, port)

    started = time.perf_counter()
    process = subprocess.Popen(
        [sys.executable, "-m", "pyignite", "run"],
        cwd=project_dir,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        time.sleep(1.5)
        if process.poll() is not None:
            stderr = process.stderr.read() if process.stderr else ""
            stdout = process.stdout.read() if process.stdout else ""
            raise RuntimeError(f"run process exited early\n{stdout}\n{stderr}")
        elapsed_ms = (time.perf_counter() - started) * 1000
    finally:
        process.terminate()
        process.wait(timeout=5)
    return elapsed_ms


def _measure_incremental_feedback_cycle(*, project_dir: Path, repo_root: Path) -> float:
    env = _bench_env(repo_root)
    test_file = project_dir / "tests" / "test_health.py"
    original = test_file.read_text(encoding="utf-8")
    test_file.write_text(original + "\n", encoding="utf-8")

    started = time.perf_counter()
    _run(
        [sys.executable, "-m", "pyignite", "lint", "check", "tests/test_health.py"],
        cwd=project_dir,
        env=env,
        timeout=120,
    )
    _run(
        [sys.executable, "-m", "pyignite", "test", "tests/test_health.py"],
        cwd=project_dir,
        env=env,
        timeout=120,
    )
    elapsed_ms = (time.perf_counter() - started) * 1000

    test_file.write_text(original, encoding="utf-8")
    return elapsed_ms


def _run(command: list[str], *, cwd: Path, env: dict[str, str], timeout: int) -> None:
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    if completed.returncode == 0:
        return
    combined = (completed.stdout or "") + (completed.stderr or "")
    raise RuntimeError(f"Command failed ({completed.returncode}): {' '.join(command)}\n{combined}")


def _bench_env(repo_root: Path) -> dict[str, str]:
    env = dict(os.environ)
    src_path = str(repo_root / "src")
    current = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{src_path}:{current}" if current else src_path
    return env


def _free_port() -> int:
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _set_run_port(config_path: Path, port: int) -> None:
    lines = config_path.read_text(encoding="utf-8").splitlines()
    updated: list[str] = []
    in_run = False
    replaced = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            in_run = stripped == "[run]"
        if in_run and stripped.startswith("port ="):
            updated.append(f"port = {port}")
            replaced = True
            continue
        updated.append(line)

    if not replaced:
        raise RuntimeError("Could not locate `[run].port` in pyignite.toml")

    config_path.write_text("\n".join(updated) + "\n", encoding="utf-8")


def _percentile(values: list[float], quantile: float) -> float:
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    index = int(round((len(ordered) - 1) * quantile))
    return ordered[index]


def _git_head(repo_root: Path) -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    if completed.returncode != 0:
        return "unknown"
    return completed.stdout.strip() or "unknown"


if __name__ == "__main__":
    main()
