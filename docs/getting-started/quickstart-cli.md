# CLI Quickstart

[Project README](../../README.md) · [Docs Index](../README.md) · [Getting Started](README.md)

Goal: create and validate your first Flint Python CLI project.

Need CLI installation first? Use the [Install guide](install.md).

## Prerequisites

- Python 3.12+
- `uv` installed and available in `PATH`

## 1) Create a new CLI project

```bash
flint new mycli --profile cli
cd mycli
```

Expected result:

- `src/` package scaffold generated with CLI entrypoint
- baseline test file generated
- `flint.toml` contains `profile = "cli"`

## 2) Install dependencies

```bash
uv sync --extra dev
```

Expected result:

- virtual environment created
- dev tooling installed (`pytest`, `ruff`, `pyright`)

## 3) Run the CLI and quality flow

```bash
flint run
flint dev
flint test
flint check
```

Expected result:

- `run` executes the generated CLI entrypoint
- `dev` starts checks-only watch mode for fast feedback
- baseline CLI test passes
- `check` pipeline completes with deterministic status output

## Success checklist

- [ ] `flint new --profile cli` generated project successfully
- [ ] dependencies installed with `uv sync --extra dev`
- [ ] `flint run` executes successfully
- [ ] `flint test` passes
- [ ] `flint check` passes

## See Also

- [Getting Started index](README.md)
- [Install guide](install.md)
- [Troubleshooting](troubleshooting-alpha.md)
