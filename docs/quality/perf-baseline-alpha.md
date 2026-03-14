# Performance Baseline

[Project README](../../README.md) · [Docs Index](../README.md) · [Quality and Performance](README.md)

Baseline artifacts:

- local/dev baseline: `benchmarks/baseline.alpha.json`
- GitHub-hosted CI baseline: `benchmarks/baseline.github-hosted.alpha.json`

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

These values serve as the M4 guardrail reference and can be updated with explicit rationale when expected performance changes land.

CI note: GitHub-hosted runners have materially higher variance on incremental test feedback timing than local captures. Use the CI baseline when comparing results captured in GitHub Actions.

## See Also

- [Quality and Performance index](README.md)
- [Performance benchmarks](perf-benchmarks.md)
