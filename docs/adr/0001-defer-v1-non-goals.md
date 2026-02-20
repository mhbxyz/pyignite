# ADR 0001: Defer v1 Non-Goals

[Project README](../../README.md) · [Docs Index](../README.md) · [ADR Index](README.md)

- Status: Accepted
- Date: 2026-02-19
- Owners: PyIgnite maintainers
- Related: [Command contract v1](../reference/command-contract-v1.md), milestone M1 issue #1

## See Also

- [ADR index](README.md)
- [ADR 0002](0002-standalone-cli-delegated-packaging.md)

## Context

PyIgnite v1 alpha optimizes for fast delivery of a reliable command surface for API teams. Expanding scope too early risks instability in core CLI behavior and slows milestone delivery.

## Decision

The following capabilities are explicitly deferred beyond v1 alpha:

1. Plugin API ecosystem.
2. Flask/Litestar framework parity.
3. Database scaffolding by default.
4. Advanced CI generation.

## Rationale

- Core value in v1 is deterministic local workflow (`new`, `dev`, `run`, `test`, `lint`, `fmt`, `check`).
- Deferred items introduce design surface area (extension points, framework abstractions, template variants, CI matrix complexity) that is not required to validate product promise.
- Limiting scope reduces regression risk and preserves implementation velocity for M1-M3.

## Reopen Conditions

Any deferred item can be reconsidered when all conditions are met:

- M1-M3 core command behavior is stable and documented.
- Internal alpha feedback identifies the item as recurring blocker for target users.
- A dedicated issue defines measurable acceptance criteria and explicit out-of-scope boundary.
- The change does not break v1 command contract backward compatibility without a versioned migration note.

## Consequences

- Positive: stronger focus, faster milestones, clearer decision boundaries in triage.
- Negative: some teams will need temporary manual setup for non-core needs.
- Operational: new issues proposing deferred scope must reference this ADR and justify reopen criteria.
