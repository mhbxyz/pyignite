# Alpha Performance Baseline

Baseline artifact: `benchmarks/baseline.alpha.json`

Reference environment from baseline capture:

- Python: 3.12.12
- Platform: linux
- Commit: `4e8edc6`

## Baseline metrics

- `startup_run`
  - p50: 1500.70 ms
  - p95: 1500.86 ms
- `save_to_feedback_incremental_test_change`
  - p50: 582.73 ms
  - p95: 845.76 ms

These values serve as the initial M4 guardrail reference and can be updated with explicit rationale when expected performance changes land.
