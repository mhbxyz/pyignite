# PyQuick

PyQuick is the developer toolchain for Python projects.

## TL;DR

```bash
pipx install pyqck
pyqck new myapi --profile api --template fastapi
cd myapi
pyqck install
pyqck test
pyqck check
```

## Core Commands

```bash
pyqck new <name> --profile <api|lib|cli> [--template ...]
pyqck install
pyqck sync
pyqck dev
pyqck run
pyqck test
pyqck lint
pyqck fmt
pyqck check
```

## Quick Navigation

- Docs index: [docs/README.md](docs/README.md)
- Install guide: [docs/getting-started/install.md](docs/getting-started/install.md)
- API quickstart (baseline): [docs/getting-started/quickstart-alpha.md](docs/getting-started/quickstart-alpha.md)
- Library quickstart: [docs/getting-started/quickstart-lib.md](docs/getting-started/quickstart-lib.md)
- CLI quickstart: [docs/getting-started/quickstart-cli.md](docs/getting-started/quickstart-cli.md)
- Troubleshooting: [docs/getting-started/troubleshooting-alpha.md](docs/getting-started/troubleshooting-alpha.md)
- Release checklist: [docs/release/release-alpha-checklist.md](docs/release/release-alpha-checklist.md)

## Docs by Section

- Getting Started: [docs/getting-started/README.md](docs/getting-started/README.md)
- Reference: [docs/reference/README.md](docs/reference/README.md)
- Dev Loop: [docs/dev-loop/README.md](docs/dev-loop/README.md)
- Quality and Performance: [docs/quality/README.md](docs/quality/README.md)
- Release and Feedback: [docs/release/README.md](docs/release/README.md)
- Architecture Decisions: [docs/adr/README.md](docs/adr/README.md)

## Product Scope (v1 alpha)

- Profile-based scaffolding for `api`, `lib`, and `cli` projects
- API profile is the most mature alpha baseline today
- No DB scaffolding by default
- Deterministic local checks via `pyqck test` and `pyqck check` across profiles
- Profile-aware `run`/`dev` behavior is being finalized (tracked in #34)

## Roadmap

1. M1 - Foundations (CLI + Config)
2. M2 - FastAPI Scaffold (No DB)
3. M3 - Dev Loop (Vite-like)
4. M4 - Quality, Perf, DX Hardening
5. M5 - Internal Alpha Release

## License

MIT
