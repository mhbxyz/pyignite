# Alpha Triage Process

This process converts internal alpha feedback into prioritized product work.

## Intake channel

- Primary channel: GitHub issues using `.github/ISSUE_TEMPLATE/alpha-feedback.yml`
- Required labels on intake:
  - `feedback:alpha`
  - `stage:alpha`

## Triage cadence and SLA

- Triage cycle: weekly (or earlier for blockers)
- Initial classification SLA: within 48 hours
- Blocker response target: same business day

## Triage workflow

1. Intake issue created with template fields.
2. Triage owner validates reproducibility and scope.
3. Apply rubric score and map to priority.
4. Assign disposition:
   - fix-now
   - schedule-post-alpha
   - needs-more-info
   - not-planned (with rationale)
5. Link to follow-up implementation issue if accepted.

## Status model

- `new`: created, not yet triaged
- `triaged`: rubric applied and disposition selected
- `blocked/release-critical`: impacts release readiness
- `scheduled/post-alpha`: accepted for roadmap
- `closed/no-action`: not planned or duplicate, with rationale

## Rubric

Score each item by severity, frequency, impact area, and reproduction confidence.

### Severity

- blocker = 4
- high = 3
- medium = 2
- low = 1

### Frequency

- always = 3
- often = 2
- sometimes = 1
- once = 0

### User impact area

- core workflow (`new`, `run`, `dev`, `test`, `check`) = 3
- docs/perf/supporting = 2
- minor polish = 1

### Reproduction confidence

- stable repro = 2
- intermittent = 1
- unclear = 0

### Priority mapping

- total >= 10 -> `priority:P0`
- total 7-9 -> `priority:P1`
- total 4-6 -> `priority:P2`
- total <= 3 -> `priority:P3`

## Triage outputs per cycle

At the end of each triage cycle, publish:

- top blockers list
- accepted follow-up issues with priority
- deferred items with rationale

Update `docs/release/post-alpha-roadmap.md` with ranked items from the latest cycle.
