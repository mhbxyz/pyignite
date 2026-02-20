from pyignite.devloop.renderer import CycleSummary, DevLoopRenderer


class Sink:
    def __init__(self) -> None:
        self.lines: list[str] = []

    def secho(self, message: str, **kwargs) -> None:
        err = kwargs.get("err", False)
        prefix = "ERR" if err else "OUT"
        self.lines.append(f"{prefix}:{message}")

    def echo(self, message: str, **kwargs) -> None:
        err = kwargs.get("err", False)
        prefix = "ERR" if err else "OUT"
        self.lines.append(f"{prefix}:{message}")


def test_renderer_happy_path_snapshot() -> None:
    sink = Sink()
    renderer = DevLoopRenderer(secho=sink.secho, echo=sink.echo)

    renderer.loop_started(("src", "tests"), 200)
    renderer.server_started(("uv", "run", "uvicorn", "myapi.main:app"))
    renderer.cycle_started(1, ["src/app.py", "tests/test_app.py"])
    renderer.checks_plan("incremental", "path-targeted", ["lint", "type", "test"])
    renderer.step_started("lint")
    renderer.step_ok("lint", 45)
    renderer.step_started("type")
    renderer.step_ok("type", 90)
    renderer.step_started("test")
    renderer.step_ok("test", 120)
    renderer.cycle_summary(
        CycleSummary(
            cycle=1,
            changed_files=("src/app.py", "tests/test_app.py"),
            plan_mode="incremental",
            plan_reason="path-targeted",
            steps_run=("lint", "type", "test"),
            failed_step=None,
            duration_ms=290,
        )
    )

    assert sink.lines == [
        "OUT:Dev loop started",
        "OUT:Watching src, tests (debounce 200ms)",
        "OUT:Server up: uv run uvicorn myapi.main:app",
        "OUT:Cycle #1: 2 change(s): src/app.py, tests/test_app.py",
        "OUT:Checks: incremental (path-targeted) -> lint -> type -> test",
        "OUT:Run [lint]",
        "OUT:OK [lint] 45ms",
        "OUT:Run [type]",
        "OUT:OK [type] 90ms",
        "OUT:Run [test]",
        "OUT:OK [test] 120ms",
        "OUT:Summary #1: passed (lint, type, test) in 290ms",
    ]


def test_renderer_failure_snapshot() -> None:
    sink = Sink()
    renderer = DevLoopRenderer(secho=sink.secho, echo=sink.echo)

    renderer.cycle_started(3, ["src/service.py", "src/repo.py", "src/api.py", "tests/test_api.py"])
    renderer.checks_plan("full", "threshold", ["lint", "type", "test"])
    renderer.step_started("lint")
    renderer.step_failed("lint", 1, 52, ("src/service.py:10:5 F401 unused import",))
    renderer.cycle_summary(
        CycleSummary(
            cycle=3,
            changed_files=("src/service.py",),
            plan_mode="full",
            plan_reason="threshold",
            steps_run=("lint",),
            failed_step="lint",
            duration_ms=70,
        )
    )

    assert sink.lines == [
        "OUT:Cycle #3: 4 change(s): src/service.py, src/repo.py, src/api.py",
        "OUT:... +1 more file(s)",
        "OUT:Checks: full (threshold) -> lint -> type -> test",
        "OUT:Run [lint]",
        "ERR:FAILED [lint] exit 1 (52ms)",
        "ERR:Details:",
        "ERR:src/service.py:10:5 F401 unused import",
        "ERR:Hint: run `pyignite lint` for full output.",
        "ERR:Summary #3: failed on lint after 70ms",
    ]
