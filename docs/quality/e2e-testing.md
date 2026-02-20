# E2E Testing Guide

End-to-end tests validate the core API workflow across command boundaries.

## Command target

Run only E2E tests:

```bash
scripts/run_e2e.sh
```

Equivalent direct command:

```bash
uv run pytest tests/e2e
```

## Prerequisites

- `uv` installed and available in `PATH`
- Python 3.12+
- local network loopback available (`127.0.0.1`)

## Flakiness mitigation notes

- E2E tests use isolated temp directories per scenario.
- `pyignite run` smoke checks use a dynamically selected free port.
- long-running server process is terminated explicitly after startup validation.
- subprocess calls use explicit timeouts to avoid hangs.
- assertions focus on deterministic diagnostics (`ERROR [config]`, `ERROR [tooling]`, `Hint:`).

## Debug tips

- rerun only failing file:

```bash
uv run pytest tests/e2e/test_api_workflow_e2e.py -q
```

- keep stdout/stderr visible:

```bash
uv run pytest tests/e2e -s
```
