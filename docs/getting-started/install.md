# Install Flint CLI

[Project README](../../README.md) · [Docs Index](../README.md) · [Getting Started](README.md)

Goal: install `flint` and verify `flint --help` works in your shell.

## Choose an install mode

- **Global CLI (`pipx`)**: best for running `flint` from anywhere in your shell `PATH`
- **Project-local (`venv` + `pip`)**: best when each repository should pin its own tool version

## Option A) Global install with `pipx`

Use this when you want one shared `flint` command across projects.

### Prerequisites

- Python 3.12+
- `pipx` installed

### Install

```bash
pipx install flint-dev
```

### Verify

```bash
flint --help
```

Expected result:

- help output prints successfully
- `flint` is available directly from your shell

### Install `uv`

Flint does not install `uv` automatically. Install it separately before running project commands such as `flint test`, `flint run`, or `flint dev`.

Recommended next step:

```bash
pipx install uv
```

## Option B) Project-local install with `venv` and `pip`

Use this when you want a per-project CLI installation.

### Prerequisites

- Python 3.12+

### Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install

```bash
pip install flint-dev
```

### Verify

```bash
flint --help
```

Expected result:

- help output prints successfully
- `flint` resolves from active virtual environment

### Install `uv`

Flint does not install `uv` automatically. Install it separately before running project commands such as `flint test`, `flint run`, or `flint dev`.

Recommended next step:

```bash
pip install uv
```

## Upgrade

Global (`pipx`):

```bash
pipx upgrade flint-dev
```

Project-local (`venv`):

```bash
pip install --upgrade flint-dev
```

## Uninstall

Global (`pipx`):

```bash
pipx uninstall flint-dev
```

Project-local (`venv`):

```bash
pip uninstall flint-dev
```

## Troubleshooting

### `flint: command not found`

Common causes:

- `pipx` binary path is not exported in your shell
- venv is not activated for project-local usage

Fix:

1. run `pipx ensurepath`
2. restart your shell session
3. for local installs, run `source .venv/bin/activate`
4. retry `flint --help`

### Wrong Python version

Symptom:

- install or runtime errors mentioning unsupported Python

Fix:

1. run `python --version`
2. use Python 3.12+
3. reinstall after switching interpreter

### Installed but command still unavailable

Fix:

1. confirm install state (`pipx list` or `pip show flint-dev` in active venv)
2. verify your active shell and environment activation
3. rerun verification: `flint --help`

### `uv: command not found`

Common causes:

- `uv` is not installed yet
- `uv` is installed but not available in your shell `PATH`

Fix:

1. install `uv` (`pipx install uv` or `pip install uv`)
2. verify `uv --version`
3. run `uv sync --extra dev` in your project

## Next step

After install succeeds, continue with [Quickstart](quickstart-alpha.md).
