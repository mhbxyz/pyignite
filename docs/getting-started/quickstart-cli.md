# CLI Quickstart

[Project README](../../README.md) · [Docs Index](../README.md) · [Getting Started](README.md)

Goal: create and validate your first PyQuick Python CLI project.

Need CLI installation first? Use the [Install guide](install.md).

## Prerequisites

- Python 3.12+
- `uv` installed and available in `PATH`

## 1) Create a new CLI project

```bash
pyqck new mycli --profile cli
cd mycli
```

Expected result:

- `src/` package scaffold generated with CLI entrypoint
- baseline test file generated
- `pyquick.toml` contains `profile = "cli"`

## 2) Install dependencies

```bash
pyqck install
```

Expected result:

- virtual environment created
- dev tooling installed (`pytest`, `ruff`, `pyright`)

## 3) Run baseline quality flow

```bash
pyqck test
pyqck check
```

Expected result:

- baseline CLI test passes
- `check` pipeline completes with deterministic status output

Note: profile-aware `pyqck run`/`pyqck dev` behavior for CLI projects is tracked in issue #34.

## Success checklist

- [ ] `pyqck new --profile cli` generated project successfully
- [ ] dependencies installed with `pyqck install`
- [ ] `pyqck test` passes
- [ ] `pyqck check` passes

## See Also

- [Getting Started index](README.md)
- [Install guide](install.md)
- [Alpha troubleshooting](troubleshooting-alpha.md)
