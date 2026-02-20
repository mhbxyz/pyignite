# Dev Loop Terminal UX

This document defines the `pyignite dev` output model for long-running sessions.

## Goals

- Quickly answer: what changed, what ran, what failed.
- Keep output clean across long sessions.
- Provide immediate next action when failures happen.

## Output model

Each change burst emits one cycle:

1. Cycle header with changed files
2. Check plan summary (`incremental` or `full`, plus reason)
3. Step execution lines (`Run`, `OK`, `FAILED`)
4. Single cycle summary line

## Example (success)

```text
Dev loop started
Watching src, tests (debounce 200ms)
Server up: uv run uvicorn myapi.main:app --host 127.0.0.1 --port 8000
Cycle #4: 2 change(s): src/users.py, tests/test_users.py
Checks: incremental (path-targeted) -> lint -> type -> test
Run [lint]
OK [lint] 44ms
Run [type]
OK [type] 97ms
Run [test]
OK [test] 131ms
Summary #4: passed (lint, type, test) in 305ms
```

## Example (failure)

```text
Cycle #6: 1 change(s): src/service.py
Checks: incremental (path-targeted) -> lint -> type -> test
Run [lint]
FAILED [lint] exit 1 (53ms)
Details:
src/service.py:10:5 F401 unused import
Hint: run `pyignite lint` for full output.
Summary #6: failed on lint after 70ms
```

## Noise control rules

- Limit changed file preview to first 3 files, then summarize the remainder.
- Print compact details excerpt (max 8 non-empty lines) on failed steps.
- Avoid full tool logs during successful steps.
