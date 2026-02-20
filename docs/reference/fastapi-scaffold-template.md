# FastAPI Scaffold Template (No DB)

[Project README](../../README.md) · [Docs Index](../README.md) · [Reference](README.md)

This document defines the generated structure for the v1 FastAPI scaffold profile.

## Generated layout

```text
.
├── .gitignore
├── README.md
├── pyproject.toml
├── pyignite.toml
├── src/
│   └── <project_package>/
│       ├── __init__.py
│       ├── main.py
│       └── api/
│           ├── __init__.py
│           ├── health.py
│           └── router.py
└── tests/
    ├── __init__.py
    └── test_health.py
```

`<project_package>` is derived from the project name and normalized to a valid Python package identifier.

## Runtime convention

- `run.app` defaults to `<project_package>.main:app`
- Host/port defaults remain in `pyignite.toml`
- `GET /health` returns deterministic JSON: `{"status": "ok"}`

## Extension points

- Add new API routes under `src/<project_package>/api/`
- Split router modules by domain and include them from `router.py`
- Add tests in `tests/` as routes/features are added

## Explicit non-goal

No database stack is generated in this template:

- no ORM dependencies
- no migration setup
- no DB connection configuration

## See Also

- [Reference index](README.md)
- [Command contract v1](command-contract-v1.md)
