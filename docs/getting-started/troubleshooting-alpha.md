# Troubleshooting

[Project README](../../README.md) · [Docs Index](../README.md) · [Getting Started](README.md)

Use this guide when the quickstart flow fails.

For install/setup issues before quickstart, start with [Install guide](install.md).

## Why can I run `flint ...` directly?

Flint delegates environment/package execution to `uv` while keeping Flint as the standalone workflow CLI.

- `flint` handles orchestration and diagnostics
- `uv` handles environment and tool execution consistency

See [ADR 0002](../adr/0002-standalone-cli-delegated-packaging.md) for the architecture decision.

## `ERROR [config]` when running commands

Symptoms:

- command exits with code `2`
- output shows `ERROR [config] ...` then `Hint:`

Common causes:

- invalid TOML syntax in `flint.toml`
- unsupported keys or wrong value types
- invalid values (for example wrong `checks_mode`, invalid port)

Fix:

1. check `flint.toml` formatting
2. compare against [reference config example](../reference/examples/flint.toml)
3. retry the command

## `ERROR [tooling]` about missing tool/runner

Symptoms:

- output references missing runner/tool executable
- command exits non-zero

Common causes:

- `uv` not installed or not in `PATH`
- dependencies not installed in project
- tooling config points to a non-existent executable

Fix:

1. ensure `uv --version` works
2. run `uv sync --extra dev` in project root
3. verify `[tooling]` values in `flint.toml`

## `flint run` fails to boot app

Symptoms:

- `ERROR [tooling] Failed to run ASGI app ...`
- uvicorn import/app errors in output

Common causes:

- `[run].app` points to wrong module path
- module exists but no `app` object exported
- port already in use

Fix:

1. verify `run.app` matches `src/<package>/main.py` path
2. ensure an `app` variable exists
3. change `[run].port` if needed

## `flint dev` feels noisy or slow

Symptoms:

- frequent full check runs
- long save-to-feedback cycles

Common causes:

- fallback to full mode triggered by config changes
- low `fallback_threshold`
- large multi-file edits

Fix:

1. review [Dev Loop incremental checks](../dev-loop/incremental-checks.md)
2. set `[dev].checks_mode = "incremental"`
3. tune `[dev].fallback_threshold` as needed

## E2E tests are flaky locally

Symptoms:

- intermittent failures in `tests/e2e`

Fix:

1. run on an idle machine/session
2. rerun with logs: `uv run pytest tests/e2e -s`
3. use file-level rerun to isolate one profile/validation suite:
   - `uv run pytest tests/e2e/test_api_workflow_e2e.py -q`
   - `uv run pytest tests/e2e/test_lib_workflow_e2e.py -q`
   - `uv run pytest tests/e2e/test_cli_workflow_e2e.py -q`
   - `uv run pytest tests/e2e/test_profile_template_validation_e2e.py -q`

## Still blocked?

Report the issue on GitHub with reproduction steps so maintainers can reproduce quickly.

## See Also

- [Getting Started index](README.md)
- [Install guide](install.md)
- [Quickstart](quickstart-alpha.md)
