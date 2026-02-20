# Performance Benchmarks

[Project README](../../README.md) · [Docs Index](../README.md) · [Quality and Performance](README.md)

PyIgnite includes repeatable performance scenarios and regression guardrails.

## Scenarios

- `startup_run`: end-to-end startup latency for `pyignite run` in a generated sample project.
- `save_to_feedback_incremental_test_change`: incremental feedback latency for a test-file change (`lint` + targeted `test`).

## Run benchmarks locally

```bash
scripts/run_benchmarks.sh
```

This command:

1. Generates `benchmarks/current.alpha.json` via runtime measurements.
2. Compares results against `benchmarks/baseline.alpha.json`.
3. Fails if any `p50` or `p95` regression exceeds 30%.

## Regenerating baseline

When intentional performance changes are accepted:

1. Run `uv run python scripts/benchmark_runtime.py --output benchmarks/current.alpha.json`.
2. Review deltas with `uv run python scripts/benchmark_compare.py benchmarks/baseline.alpha.json benchmarks/current.alpha.json`.
3. Copy current results into `benchmarks/baseline.alpha.json` in the same commit that explains the change.

## Notes on variability

- Benchmarks run on local hardware and include subprocess overhead.
- Expect small variance between runs; guardrails are tuned for significant regressions.
- Run on an idle machine when possible for stable measurements.

## See Also

- [Quality and Performance index](README.md)
- [Alpha performance baseline](perf-baseline-alpha.md)
