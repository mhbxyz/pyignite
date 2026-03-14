# Quickstart

[Project README](../../README.md) · [Docs Index](../README.md) · [Getting Started](README.md)

Goal: run your first Flint API project in under 10 minutes.

Need CLI installation first? Use the [Install guide](install.md).

## Execution model (important)

Flint is a standalone workflow CLI, and dependency/environment execution is delegated to `uv`.

- Bootstrap from anywhere: `flint new ...`
- Inside generated projects: run workflow commands directly (`flint ...`)

Why this split?

- deterministic tool versions from project lock/env
- consistent behavior across contributors and CI
- explicit separation of concerns (`flint` orchestration, `uv` tool runtime)

## Prerequisites

- Python 3.12+
- `uv` installed and available in `PATH`
- local shell with write access to your workspace

## 1) Create a new API project

```bash
flint new myapi --profile api --template fastapi
cd myapi
```

Expected result:

- project files generated
- `src/` layout ready
- `flint.toml` present

## 2) Prepare the project environment

```bash
uv sync --extra dev
```

Expected result:

- virtual environment resolved
- runtime + dev tools installed

## 3) Start the API

```bash
flint run
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
flint dev
```

Expected result:

- file changes in `src/` or `tests/` trigger reload and checks
- terminal shows cycle summaries and step outcomes

## 5) Validate quality gates

```bash
flint test
flint check
```

Expected result:

- baseline health test passes
- check pipeline finishes with deterministic status output

## Success checklist

- [ ] `flint new` generated project successfully
- [ ] project environment prepared with `uv sync --extra dev`
- [ ] `/health` returns `{"status": "ok"}`
- [ ] `flint dev` reacts to file changes
- [ ] `flint test` and `flint check` pass

## If something fails

Use [Troubleshooting](troubleshooting-alpha.md) for common fixes, then open a GitHub issue with reproduction steps.

## See Also

- [Getting Started index](README.md)
- [Install guide](install.md)
