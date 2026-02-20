# Dev Loop Incremental Checks

[Project README](../../README.md) · [Docs Index](../README.md) · [Dev Loop](README.md)

PyQuick uses staged feedback in `pyqck dev` to keep save-to-feedback fast while preserving correctness.

## Modes

- `incremental` (default): target checks by changed paths when safe.
- `full`: always run full checks (`lint`, `type`, `test`) on every save.

Configure in `pyquick.toml`:

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

PyQuick falls back to full checks when uncertainty is high, including:

- config/tooling file changes (`pyproject.toml`, `pyquick.toml`, `ruff*.toml`, `pyrightconfig.json`)
- changed file count exceeds `fallback_threshold`
- Python changes outside known `src/` / `tests/` scopes

This avoids silent misses while keeping common save cycles fast.

## Baseline comparison

Use the benchmark helper to compare baseline full checks versus incremental planning on representative change sets:

```bash
uv run python scripts/benchmark_devloop_checks.py
```

The script prints aggregate baseline vs incremental cost estimates using fixed per-step cost assumptions.

## See Also

- [Dev Loop index](README.md)
- [Terminal UX model](terminal-ux.md)
