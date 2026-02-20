from __future__ import annotations

from pyignite.devloop.incremental import CHECKS_MODE_INCREMENTAL, resolve_check_plan

STEP_COST_SECONDS = {
    "lint": 0.35,
    "type": 0.70,
    "test": 1.10,
}

CHANGE_SETS = [
    ["tests/test_health.py"],
    ["tests/test_users.py"],
    ["src/myapi/api/router.py"],
    ["src/myapi/service.py", "tests/test_service.py"],
    ["pyproject.toml"],
]


def _full_cost() -> float:
    return STEP_COST_SECONDS["lint"] + STEP_COST_SECONDS["type"] + STEP_COST_SECONDS["test"]


def _plan_cost(changed_files: list[str]) -> float:
    plan = resolve_check_plan(
        changed_files,
        checks_mode=CHECKS_MODE_INCREMENTAL,
        fallback_threshold=8,
    )
    return sum(STEP_COST_SECONDS[step.name] for step in plan.steps)


def main() -> None:
    baseline_total = sum(_full_cost() for _ in CHANGE_SETS)
    incremental_total = sum(_plan_cost(change_set) for change_set in CHANGE_SETS)
    reduction = ((baseline_total - incremental_total) / baseline_total) * 100

    print("Benchmark: baseline full checks vs incremental plan")
    print(f"Samples: {len(CHANGE_SETS)} change sets")
    print(f"Baseline total: {baseline_total:.2f}s")
    print(f"Incremental total: {incremental_total:.2f}s")
    print(f"Estimated reduction: {reduction:.1f}%")


if __name__ == "__main__":
    main()
