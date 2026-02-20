# ADR 0002: Standalone CLI, Delegated Packaging Backend

- Status: Accepted
- Date: 2026-02-20
- Owners: PyIgnite maintainers
- Related: `docs/getting-started/quickstart-alpha.md`, milestone M5 planning

## Context

PyIgnite aims to feel like a standalone product CLI. Current alpha workflows rely on `uv` for environment and package operations (`uv sync`, `uv run`). Without an explicit decision, users can perceive this as contradictory: standalone UX versus delegated runtime execution.

## Decision

1. PyIgnite remains a standalone orchestration CLI at product/UX level.
2. PyIgnite does not become a package manager.
3. Packaging and environment execution are delegated to a backend, with `uv` as the only official backend during alpha.
4. `pyignite install` will be introduced in M5 as a user-facing wrapper over backend sync operations.

## Responsibility Boundary

- `pyignite` owns:
  - command workflows (`new`, `dev`, `run`, `test`, `lint`, `fmt`, `check`)
  - project conventions and defaults
  - diagnostics and actionable errors
- packaging backend (`uv` in alpha) owns:
  - dependency resolution and lock/install behavior
  - virtual environment management
  - command execution inside project environment

## Consequences

- Positive:
  - clear product boundary and maintainable architecture
  - easier future backend abstraction without changing user workflows
  - keeps PyIgnite focused on developer experience and orchestration
- Tradeoff:
  - alpha docs must explicitly explain why project-local commands route through `uv`

## Implementation Notes

- Alpha (now): keep `uv` as required backend and document execution model clearly.
- M5:
  - add `pyignite install` wrapper command
  - define backend interface (`sync`, `exec_tool`, `doctor`) behind command execution
  - retain strict determinism and actionable failure diagnostics
