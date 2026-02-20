from pyignite.devloop.incremental import (
    CHECKS_MODE_FULL,
    CHECKS_MODE_INCREMENTAL,
    resolve_check_plan,
)


def test_incremental_plan_targets_test_file_only_changes() -> None:
    plan = resolve_check_plan(
        ["tests/test_api.py"],
        checks_mode=CHECKS_MODE_INCREMENTAL,
        fallback_threshold=8,
    )

    assert plan.mode == "incremental"
    assert [step.name for step in plan.steps] == ["lint", "test"]
    assert plan.steps[0].args == ("check", "tests/test_api.py")
    assert plan.steps[1].args == ("tests/test_api.py",)


def test_incremental_plan_falls_back_to_full_on_config_change() -> None:
    plan = resolve_check_plan(
        ["pyproject.toml"],
        checks_mode=CHECKS_MODE_INCREMENTAL,
        fallback_threshold=8,
    )

    assert plan.mode == "full"
    assert plan.reason == "config-change"
    assert [step.name for step in plan.steps] == ["lint", "type", "test"]


def test_incremental_plan_falls_back_to_full_on_large_change_set() -> None:
    changed = [f"src/pkg/mod_{idx}.py" for idx in range(10)]
    plan = resolve_check_plan(
        changed,
        checks_mode=CHECKS_MODE_INCREMENTAL,
        fallback_threshold=5,
    )

    assert plan.mode == "full"
    assert plan.reason == "threshold"


def test_full_mode_forces_full_pipeline() -> None:
    plan = resolve_check_plan(
        ["tests/test_api.py"],
        checks_mode=CHECKS_MODE_FULL,
        fallback_threshold=8,
    )

    assert plan.mode == "full"
    assert plan.reason == "forced-full"
    assert [step.name for step in plan.steps] == ["lint", "type", "test"]
