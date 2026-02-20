#!/usr/bin/env bash
set -euo pipefail

uv run python scripts/benchmark_runtime.py --output benchmarks/current.alpha.json
uv run python scripts/benchmark_compare.py benchmarks/baseline.alpha.json benchmarks/current.alpha.json 30
