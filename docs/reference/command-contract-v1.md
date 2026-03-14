# Flint v1 Command Contract

## Commands

### `flint run`

- Purpose: start the project's canonical ASGI app
- Resolution order: `flint.toml`, then repo conventions
- Success: starts the app process and exits `0` when it ends cleanly
- Failure:
  - exit `2` for invalid config or unresolved app target
  - exit `1` for subprocess or tool failure

### `flint dev`

- Purpose: start the app plus a watch-driven validation loop
- Behavior:
  - starts the ASGI app without nested framework reloaders
  - restarts the app on source or config changes
  - reruns checks on source, test, or config changes
- Success: exits `0` on clean user stop
- Failure:
  - exit `2` for invalid config or unresolved app target
  - exit `1` for watcher or subprocess failure

### `flint check`

- Purpose: run the deterministic local quality gate
- Order: `ruff`, `pytest`, optional `pyright`
- Success: all stages pass and exit `0`
- Failure:
  - exit `2` for invalid config
  - exit `1` for any failing or unavailable tool

## Error Output

All handled failures follow this format:

```text
ERROR [category] Short explanation.
Hint: Concrete recovery step.
```

## Canonical Project Shape

The primary supported repo shape for v1 hardening is:

- `src/<package>/main.py`
- exported `app`
- `tests/`
- `pyproject.toml`
- optional `flint.toml`
