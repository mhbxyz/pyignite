# Alpha Quickstart

[Project README](../../README.md) · [Docs Index](../README.md) · [Getting Started](README.md)

Goal: run your first PyQuick API project in under 10 minutes.

## Execution model (important)

PyQuick is a standalone workflow CLI, but dependency/environment execution is delegated to `uv` in alpha.

- Bootstrap from anywhere: `pyqck new ...`
- Inside generated projects: run workflow commands through project env (`uv run pyqck ...`)

Why this split?

- deterministic tool versions from project lock/env
- consistent behavior across contributors and CI
- explicit separation of concerns (`pyqck` orchestration, `uv` packaging runtime)

## Prerequisites

- Python 3.12+
- `uv` installed and available in `PATH`
- local shell with write access to your workspace

## 1) Create a new API project

```bash
pyqck new myapi --profile api --template fastapi
cd myapi
```

Expected result:

- project files generated
- `src/` layout ready
- `pyquick.toml` present

## 2) Install dependencies

```bash
uv sync --extra dev
```

Note: a dedicated `pyqck install` wrapper is planned for M5.

Expected result:

- virtual environment resolved
- runtime + dev tools installed

## 3) Start the API

```bash
uv run pyqck run
```

Expected result:

- server starts on `127.0.0.1:8000` (unless overridden)
- `GET /health` returns `{"status": "ok"}`

Use another terminal to verify quickly:

```bash
curl http://127.0.0.1:8000/health
```

## 4) Run the dev loop

```bash
uv run pyqck dev
```

Expected result:

- file changes in `src/` or `tests/` trigger reload and checks
- terminal shows cycle summaries and step outcomes

## 5) Validate quality gates

```bash
uv run pyqck test
uv run pyqck check
```

Expected result:

- baseline health test passes
- check pipeline finishes with deterministic status output

## Success checklist

- [ ] `pyqck new` generated project successfully
- [ ] dependencies installed with `uv sync --extra dev`
- [ ] `/health` returns `{"status": "ok"}`
- [ ] `pyqck dev` reacts to file changes
- [ ] `pyqck test` and `pyqck check` pass

## If something fails

Use [Alpha troubleshooting](troubleshooting-alpha.md) for common fixes, then report issues with [Alpha feedback template](../release/alpha-feedback-template.md).

## See Also

- [Getting Started index](README.md)
- [Release and feedback docs](../release/README.md)
