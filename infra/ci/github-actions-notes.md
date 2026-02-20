# CI Notes (Scaffold)

Planned baseline pipeline stages:

- install (uv sync)
- lint (ruff check .)
- format check (ruff format --check .)
- type-check (pyright)
- test (pytest)
- e2e (`scripts/run_e2e.sh`)
- perf guardrails (`scripts/run_benchmarks.sh`, fail mode)

This file documents the intended shape before a full workflow is added.
