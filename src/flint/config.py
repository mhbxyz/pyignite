from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import tomllib

from flint.errors import config_error


@dataclass(slots=True)
class FlintConfig:
    app_module: str | None
    watch_paths: list[Path] | None
    typecheck: bool | None


@dataclass(slots=True)
class ProjectSettings:
    root: Path
    app_module: str
    watch_paths: list[Path]
    typecheck: bool


def load_project_settings(root: Path) -> ProjectSettings:
    root = root.resolve()
    config = load_flint_config(root)
    app_module = config.app_module or discover_app_module(root)
    watch_paths = resolve_watch_paths(root, config.watch_paths)
    typecheck = config.typecheck if config.typecheck is not None else should_run_typecheck(root)
    return ProjectSettings(
        root=root,
        app_module=app_module,
        watch_paths=watch_paths,
        typecheck=typecheck,
    )


def load_flint_config(root: Path) -> FlintConfig:
    config_path = root / "flint.toml"
    if not config_path.exists():
        return FlintConfig(app_module=None, watch_paths=None, typecheck=None)

    try:
        data = tomllib.loads(config_path.read_text())
    except tomllib.TOMLDecodeError as exc:
        raise config_error(
            f"Could not parse {config_path.name}.",
            "Fix the TOML syntax or remove the file and rely on conventions.",
        ) from exc

    validate_top_level_keys(data)

    app = expect_table(data, "app", optional=True)
    check = expect_table(data, "check", optional=True)
    paths = expect_table(data, "paths", optional=True)

    app_module = read_string(app, "module") if app else None
    watch_paths = read_string_list(paths, "watch", root) if paths and "watch" in paths else None
    typecheck = read_bool(check, "typecheck") if check and "typecheck" in check else None
    return FlintConfig(app_module=app_module, watch_paths=watch_paths, typecheck=typecheck)


def validate_top_level_keys(data: dict[str, Any]) -> None:
    allowed_keys = {"app", "check", "paths"}
    unknown = sorted(key for key in data if key not in allowed_keys)
    if unknown:
        raise config_error(
            f"Unknown top-level keys in flint.toml: {', '.join(unknown)}.",
            "Use only [app], [check], and [paths] in flint.toml.",
        )


def expect_table(data: dict[str, Any], key: str, optional: bool = False) -> dict[str, Any] | None:
    value = data.get(key)
    if value is None and optional:
        return None
    if value is None:
        raise config_error(f"Missing [{key}] table in flint.toml.", f"Add [{key}] or remove flint.toml.")
    if not isinstance(value, dict):
        raise config_error(f"[{key}] must be a table.", f"Rewrite [{key}] as a TOML table.")
    return value


def read_string(table: dict[str, Any], key: str) -> str:
    value = table.get(key)
    if not isinstance(value, str) or not value.strip():
        raise config_error(
            f"[{key}] must be a non-empty string.",
            f"Set `{key}` to a valid module path such as `myapp.main:app`.",
        )
    return value.strip()


def read_bool(table: dict[str, Any], key: str) -> bool:
    value = table.get(key)
    if not isinstance(value, bool):
        raise config_error(f"[{key}] must be true or false.", f"Set `{key}` to `true` or `false`.")
    return value


def read_string_list(table: dict[str, Any], key: str, root: Path) -> list[Path]:
    value = table.get(key)
    if not isinstance(value, list) or not value:
        raise config_error(
            f"[{key}] must be a non-empty array.",
            f"Set `{key}` to one or more relative paths, for example `['src', 'tests']`.",
        )

    resolved: list[Path] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise config_error(
                f"[{key}] entries must be non-empty strings.",
                f"Replace invalid `{key}` entries with relative paths.",
            )
        resolved.append((root / item).resolve())
    return resolved


def resolve_watch_paths(root: Path, configured_paths: list[Path] | None) -> list[Path]:
    if configured_paths is not None:
        return configured_paths

    candidates = [root / "src", root / "tests", root / "flint.toml", root / "pyproject.toml"]
    resolved = [path.resolve() for path in candidates if path.exists()]
    return resolved or [root]


def should_run_typecheck(root: Path) -> bool:
    pyproject_path = root / "pyproject.toml"
    if not pyproject_path.exists():
        return False

    try:
        data = tomllib.loads(pyproject_path.read_text())
    except tomllib.TOMLDecodeError:
        return False

    tool = data.get("tool", {})
    if isinstance(tool, dict) and "pyright" in tool:
        return True

    project = data.get("project", {})
    if not isinstance(project, dict):
        return False

    dependency_groups = [
        project.get("dependencies", []),
        *list((project.get("optional-dependencies", {}) or {}).values()),
    ]
    return any(_contains_pyright(group) for group in dependency_groups if isinstance(group, list))


def _contains_pyright(items: list[Any]) -> bool:
    return any(isinstance(item, str) and item.startswith("pyright") for item in items)


def discover_app_module(root: Path) -> str:
    src_main_candidates = sorted((root / "src").glob("*/main.py"))
    if len(src_main_candidates) == 1:
        return build_app_module(root, src_main_candidates[0])
    if len(src_main_candidates) > 1:
        raise config_error(
            "Found multiple ASGI app candidates under src/.",
            "Set `[app].module` in flint.toml to choose the canonical app module.",
        )

    fallback_candidates = [
        *sorted((root / "src").glob("*/app.py")),
        *sorted(root.glob("*/main.py")),
        root / "main.py",
    ]
    resolved = [candidate for candidate in fallback_candidates if candidate.exists()]
    if len(resolved) == 1:
        return build_app_module(root, resolved[0])
    if len(resolved) > 1:
        raise config_error(
            "Found multiple fallback ASGI app candidates.",
            "Set `[app].module` in flint.toml to choose the canonical app module.",
        )

    raise config_error(
        "Could not resolve an ASGI app target.",
        "Add `flint.toml` with `[app].module = 'package.main:app'` or follow the default src layout.",
    )


def build_app_module(root: Path, path: Path) -> str:
    module = module_name_from_path(root, path)
    if not module:
        raise config_error(
            "Could not resolve an importable module path for the ASGI app.",
            "Ensure the app file is inside the project root and uses a valid Python module path.",
        )
    return f"{module}:app"


def module_name_from_path(root: Path, path: Path) -> str | None:
    try:
        relative = path.resolve().relative_to(root.resolve())
    except ValueError:
        return None

    parts = list(relative.parts)
    if parts[0] == "src":
        parts = parts[1:]
    if not parts:
        return None
    parts[-1] = Path(parts[-1]).stem
    return ".".join(parts)
