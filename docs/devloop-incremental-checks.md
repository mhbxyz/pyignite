# Dev Loop Incremental Checks

PyIgnite uses staged feedback in `pyignite dev` to keep save-to-feedback fast while preserving correctness.

## Modes

- `incremental` (default): target checks by changed paths when safe.
- `full`: always run full checks (`lint`, `type`, `test`) on every save.

Configure in `pyignite.toml`:

```toml
[dev]
checks_mode = "incremental"
fallback_threshold = 8
```

## Incremental behavior

- `tests/**/*.py` only changes:
  - `ruff check` on changed files
  - `pytest` on changed test files
- `src/**/*.py` changes:
  - `ruff check` on changed files
  - `pyright` full run
  - `pytest` full run

## Automatic fallback to full checks

PyIgnite falls back to full checks when uncertainty is high, including:

- config/tooling file changes (`pyproject.toml`, `pyignite.toml`, `ruff*.toml`, `pyrightconfig.json`)
- changed file count exceeds `fallback_threshold`
- Python changes outside known `src/` / `tests/` scopes

This avoids silent misses while keeping common save cycles fast.

## Baseline comparison

Use the benchmark helper to compare baseline full checks versus incremental planning on representative change sets:

```bash
uv run python scripts/benchmark_devloop_checks.py
```

The script prints aggregate baseline vs incremental cost estimates using fixed per-step cost assumptions.
