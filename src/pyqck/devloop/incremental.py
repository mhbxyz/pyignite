from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Sequence

from pyqck.tooling import ToolKey

CHECKS_MODE_INCREMENTAL = "incremental"
CHECKS_MODE_FULL = "full"

FULL_RUN_TRIGGERS = {
    "pyproject.toml",
    "pyquick.toml",
    "ruff.toml",
    "pyrightconfig.json",
}


@dataclass(slots=True, frozen=True)
class CheckStep:
    name: str
    key: ToolKey
    args: tuple[str, ...]


@dataclass(slots=True, frozen=True)
class CheckPlan:
    mode: str
    reason: str
    steps: tuple[CheckStep, ...]


def resolve_check_plan(
    changed_files: Sequence[str],
    *,
    checks_mode: str,
    fallback_threshold: int,
) -> CheckPlan:
    normalized = tuple(sorted({_normalize_path(path) for path in changed_files if path}))
    if checks_mode == CHECKS_MODE_FULL:
        return CheckPlan(mode=CHECKS_MODE_FULL, reason="forced-full", steps=_full_steps())

    if len(normalized) > fallback_threshold:
        return CheckPlan(mode=CHECKS_MODE_FULL, reason="threshold", steps=_full_steps())

    if any(_requires_full_run(path) for path in normalized):
        return CheckPlan(mode=CHECKS_MODE_FULL, reason="config-change", steps=_full_steps())

    python_paths = tuple(path for path in normalized if path.endswith(".py"))
    if not python_paths:
        return CheckPlan(mode=CHECKS_MODE_INCREMENTAL, reason="no-python-changes", steps=())

    src_paths = tuple(path for path in python_paths if path.startswith("src/"))
    test_paths = tuple(path for path in python_paths if path.startswith("tests/"))
    other_paths = tuple(
        path for path in python_paths if path not in src_paths and path not in test_paths
    )

    if other_paths:
        return CheckPlan(mode=CHECKS_MODE_FULL, reason="unknown-python-scope", steps=_full_steps())

    steps: list[CheckStep] = [
        CheckStep(name="lint", key=ToolKey.LINTING, args=("check", *python_paths)),
    ]

    if src_paths:
        steps.append(CheckStep(name="type", key=ToolKey.TYPING, args=()))
        steps.append(CheckStep(name="test", key=ToolKey.TESTING, args=()))
    elif test_paths:
        steps.append(CheckStep(name="test", key=ToolKey.TESTING, args=test_paths))

    return CheckPlan(mode=CHECKS_MODE_INCREMENTAL, reason="path-targeted", steps=tuple(steps))


def _full_steps() -> tuple[CheckStep, ...]:
    return (
        CheckStep(name="lint", key=ToolKey.LINTING, args=("check", ".")),
        CheckStep(name="type", key=ToolKey.TYPING, args=()),
        CheckStep(name="test", key=ToolKey.TESTING, args=()),
    )


def _requires_full_run(path: str) -> bool:
    posix_path = PurePosixPath(path)
    if posix_path.name in FULL_RUN_TRIGGERS:
        return True
    if posix_path.name.startswith("ruff") and posix_path.suffix == ".toml":
        return True
    return False


def _normalize_path(path: str) -> str:
    return path.replace("\\", "/")
