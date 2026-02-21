# Binary Distribution Strategy (Issue #23)

[Project README](../../README.md) · [Docs Index](../README.md) · [Release and Feedback](README.md)

This document captures the option tradeoffs, prototype result, and rollout recommendation for standalone binary distribution.

## Evaluation Summary

| Option | Standalone without Python on target | Cross-platform practicality (alpha) | CI complexity | Notes |
| --- | --- | --- | --- | --- |
| PyInstaller | yes | high (Linux/macOS feasible now) | medium | Best balance for alpha; larger artifacts |
| Nuitka | yes | medium | high | Heavier toolchain and longer builds |
| PEX | no | high | low-medium | Great packaging, but requires Python runtime |
| shiv | no | high | low-medium | Similar to PEX; zipapp model |

## Prototype (Linux)

Prototype path: **PyInstaller one-file binary**.

Build command used:

```bash
uv run --with pyinstaller pyinstaller --onefile --name pyqck-linux --specpath /tmp src/pyqck/__main__.py --paths src
```

Measured on local Linux environment:

- Build time (clean): about `11.44s`
- Artifact: `dist/pyqck-linux`
- Artifact size: about `16M`
- Startup (`--help`) average across 5 runs: about `225ms`

Smoke flow executed successfully:

```bash
PYQCK_BIN="$PWD/dist/pyqck-linux"

"$PYQCK_BIN" --help
"$PYQCK_BIN" new smoke-api --profile api --template fastapi
cd smoke-api
"$PYQCK_BIN" install
"$PYQCK_BIN" test
```

Observed outcome:

- `new` created scaffold successfully.
- `install` completed backend sync with `OK [install]`.
- `test` completed with `OK [test]`.

## Recommendation

- **Go**: publish Linux binary artifacts as experimental GitHub Release assets.
- **Conditional go**: add macOS binary once smoke checks are green in CI.
- **No-go (for alpha)**: replacing PyPI distribution; keep `pip`/`pipx` as primary path.

## Rollout Proposal

1. Add a dedicated workflow (separate from PyPI publish) to build binary assets.
2. Upload binary artifacts to GitHub Releases with `experimental` label.
3. Keep existing TestPyPI/PyPI verification workflow as release gate of record.
4. Re-evaluate Windows support after one milestone of Linux/macOS signal.

## Risks and Mitigations

- Platform-specific breakage risk -> enforce per-platform smoke checks (`--help`, `new`, `install`, `test`).
- Artifact size increase -> publish binaries as optional assets, not default install path.
- Support burden increase -> document alpha support scope clearly in install docs.

## See Also

- [ADR 0003](../adr/0003-binary-distribution-strategy.md)
- [Releasing PyQuick](releasing.md)
- [PyPI trusted publishing](pypi-publishing.md)
