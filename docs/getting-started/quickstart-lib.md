# Library Quickstart

[Project README](../../README.md) · [Docs Index](../README.md) · [Getting Started](README.md)

Goal: create and validate your first Flint Python library project.

Need CLI installation first? Use the [Install guide](install.md).

## Prerequisites

- Python 3.12+
- `uv` installed and available in `PATH`

## 1) Create a new library project

```bash
flint new mylib --profile lib
cd mylib
```

Expected result:

- `src/` package scaffold generated
- baseline test file generated
- `flint.toml` contains `profile = "lib"`

## 2) Install dependencies

```bash
uv sync --extra dev
```

Expected result:

- virtual environment created
- dev tooling installed (`pytest`, `ruff`, `pyright`)

## 3) Run the feedback and quality flow

```bash
flint dev
flint test
flint check
```

Expected result:

- `dev` starts checks-only watch mode for fast feedback
- baseline library test passes
- `check` pipeline completes with deterministic status output

Note: `flint run` is not supported for the library profile.

## Success checklist

- [ ] `flint new --profile lib` generated project successfully
- [ ] dependencies installed with `uv sync --extra dev`
- [ ] `flint dev` starts successfully
- [ ] `flint test` passes
- [ ] `flint check` passes

## See Also

- [Getting Started index](README.md)
- [Install guide](install.md)
- [Troubleshooting](troubleshooting-alpha.md)
