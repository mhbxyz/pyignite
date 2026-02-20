from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any, cast


DEFAULT_FAIL_THRESHOLD_PERCENT = 30.0


def main() -> None:
    if len(sys.argv) < 3:
        raise SystemExit(
            "Usage: uv run python scripts/benchmark_compare.py <baseline.json> <current.json> [fail_percent]"
        )

    baseline_path = Path(sys.argv[1]).resolve()
    current_path = Path(sys.argv[2]).resolve()
    fail_threshold = float(sys.argv[3]) if len(sys.argv) >= 4 else DEFAULT_FAIL_THRESHOLD_PERCENT

    baseline = _load(baseline_path)
    current = _load(current_path)

    baseline_scenarios = cast(dict[str, dict[str, float]], baseline["scenarios"])
    current_scenarios = cast(dict[str, dict[str, float]], current["scenarios"])

    failures: list[str] = []
    print(f"Comparing benchmark results (fail threshold: {fail_threshold:.1f}%)")

    for scenario_name, baseline_metrics in baseline_scenarios.items():
        if scenario_name not in current_scenarios:
            failures.append(f"Missing scenario in current results: {scenario_name}")
            continue

        current_metrics = current_scenarios[scenario_name]
        for metric in ("p50_ms", "p95_ms"):
            baseline_value = float(baseline_metrics[metric])
            current_value = float(current_metrics[metric])
            regression = _regression_percent(baseline_value, current_value)
            print(
                f"- {scenario_name}.{metric}: baseline={baseline_value:.2f} current={current_value:.2f} "
                f"delta={regression:+.1f}%"
            )
            if regression > fail_threshold:
                failures.append(
                    f"Regression above threshold for {scenario_name}.{metric}: {regression:.1f}%"
                )

    if failures:
        print("\nPerformance guardrail failures:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print("\nPerformance guardrails passed.")


def _load(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def _regression_percent(baseline: float, current: float) -> float:
    if baseline <= 0:
        return 0.0
    return ((current - baseline) / baseline) * 100.0


if __name__ == "__main__":
    main()
