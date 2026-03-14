# Flint

Flint is an opinionated dev-loop CLI for existing Python ASGI projects.

## Product Wedge

Flint v1 is deliberately narrow:

- target existing FastAPI or Starlette style repos
- standardize the local loop around `run`, `dev`, and `check`
- delegate execution to `uv` and standard ecosystem tools

Non-goals for this first iteration:

- project scaffolding
- plugin systems
- multi-framework parity
- broad configuration surface

## Commands

```bash
flint run
flint dev
flint check
```

## Conventions

Flint resolves the ASGI app using these conventions, in order:

1. `flint.toml` with `[app].module`
2. `src/<package>/main.py` exposing `app`
3. `src/<package>/app.py` exposing `app`
4. `<package>/main.py` exposing `app`
5. `main.py` exposing `app`

Default watch paths are `src/` and `tests/` when present.

The canonical repo shape Flint optimizes for is:

- `src/<package>/main.py`
- exported ASGI object named `app`
- `tests/`
- `pyproject.toml`
- optional `flint.toml`

## Runtime Contract

- `flint run` uses `uv run uvicorn <module>:app --reload`
- `flint dev` runs the server without Uvicorn reload and restarts it when source files change
- `flint check` runs `ruff check .`, `pytest`, and optional `pyright` in that order
- missing required tools fail fast with a Flint error and a recovery hint

See [docs/reference/command-contract-v1.md](/home/mhbxyz/Projects/Flint/docs/reference/command-contract-v1.md) for the command contract.
