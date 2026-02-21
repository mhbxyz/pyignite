# ADR 0003: Binary Distribution Strategy for Alpha

[Project README](../../README.md) · [Docs Index](../README.md) · [ADR Index](README.md)

- Status: Accepted
- Date: 2026-02-21
- Owners: PyQuick maintainers
- Related: issue #23, [ADR 0002](0002-standalone-cli-delegated-packaging.md), [Binary distribution prototype](../release/binary-distribution-strategy.md)

## Context

PyQuick is currently distributed as a Python package (`pip`/`pipx`). Some users asked for standalone binaries to reduce install friction and improve first-run UX.

The team needs a decision for milestone planning: should alpha include binary artifacts in addition to PyPI distribution.

## Options Considered

1. **PyInstaller**
   - Produces a real platform binary (`onefile`/`onedir`).
   - Mature ecosystem and straightforward CI integration.
   - Tradeoff: larger artifacts and slower cold start than pure Python launch.
2. **Nuitka**
   - Compiled binaries with potential runtime performance benefits.
   - Tradeoff: heavier toolchain, longer build times, more complex cross-platform CI.
3. **PEX**
   - Good reproducible Python application bundles.
   - Tradeoff: requires Python runtime on target machine (not a true standalone binary).
4. **shiv**
   - Lightweight zipapp workflow.
   - Tradeoff: requires Python runtime on target machine (not a true standalone binary).

## Decision

1. Ship **experimental binary artifacts** as a secondary distribution channel.
2. Use **PyInstaller** as the alpha prototype and initial implementation path.
3. Keep **PyPI (`pip`/`pipx`) as the primary supported installation channel** for alpha.
4. Do **not** commit to Windows binaries in M6 unless CI stability and maintenance cost remain low after Linux/macOS rollout.

## Rationale

- PyInstaller provides the shortest path to a true standalone CLI binary with acceptable operational complexity.
- PEX/shiv are useful but do not satisfy the core standalone expectation (Python still required on target host).
- Nuitka is promising but currently too costly for alpha delivery timelines.
- A secondary-channel rollout limits risk while collecting adoption and support data.

## Prototype Outcome

Linux prototype was successfully built and smoke-tested (see linked release doc):

- Generated artifact: `dist/pyqck-linux`.
- Smoke checks passed: `--help`, `new`, `install`, `test`.
- This satisfies issue #23 prototype acceptance for at least one platform.

## Rollout Recommendation (Go/No-Go)

- **Go** for Linux experimental binary publication in release assets.
- **Conditional go** for macOS after one stable CI cycle with equivalent smoke checks.
- **No-go for replacing PyPI** in alpha; continue Python package distribution as canonical path.

## Consequences

- Positive:
  - Lower setup friction for users who prefer direct binary download.
  - Better product perception for a standalone CLI.
- Tradeoffs:
  - Additional CI jobs and artifact management.
  - Larger release assets and platform-specific support burden.

## Implementation Notes

- Add a dedicated binary build workflow separate from PyPI publish flow.
- Attach binary artifacts to GitHub Releases as `experimental` in alpha.
- Keep release verification checks unchanged for PyPI path.
- Add platform scope and limitations to install/release docs.

## See Also

- [ADR index](README.md)
- [Releasing PyQuick](../release/releasing.md)
