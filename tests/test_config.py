from pathlib import Path

import pytest

from flint.config import discover_app_module, load_flint_config, load_project_settings, should_run_typecheck
from flint.errors import FlintError


def test_load_project_settings_uses_conventions(tmp_path: Path) -> None:
    project = tmp_path
    (project / "src" / "demo").mkdir(parents=True)
    (project / "src" / "demo" / "main.py").write_text("app = object()\n")

    settings = load_project_settings(project)

    assert settings.app_module == "demo.main:app"
    assert (project / "src").resolve() in settings.watch_paths
    assert settings.typecheck is False


def test_load_flint_config_reads_overrides(tmp_path: Path) -> None:
    (tmp_path / "flint.toml").write_text(
        """
[app]
module = "custom.api:app"

[check]
typecheck = true

[paths]
watch = ["service", "tests"]
""".strip()
    )

    config = load_flint_config(tmp_path)

    assert config.app_module == "custom.api:app"
    assert config.typecheck is True
    assert config.watch_paths == [(tmp_path / "service").resolve(), (tmp_path / "tests").resolve()]


def test_invalid_flint_config_raises_config_error(tmp_path: Path) -> None:
    (tmp_path / "flint.toml").write_text("[app]\nmodule = 3\n")

    with pytest.raises(FlintError) as exc_info:
        load_flint_config(tmp_path)

    assert exc_info.value.exit_code == 2
    assert exc_info.value.category == "config"


def test_unknown_top_level_flint_config_key_raises_config_error(tmp_path: Path) -> None:
    (tmp_path / "flint.toml").write_text("[unknown]\nvalue = true\n")

    with pytest.raises(FlintError) as exc_info:
        load_flint_config(tmp_path)

    assert "Unknown top-level keys" in exc_info.value.message


def test_should_run_typecheck_from_pyproject(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        """
[project]
dependencies = ["fastapi"]

[project.optional-dependencies]
dev = ["pyright>=1.1.0"]
""".strip()
    )

    assert should_run_typecheck(tmp_path) is True


def test_discover_app_module_errors_without_convention(tmp_path: Path) -> None:
    with pytest.raises(FlintError):
        discover_app_module(tmp_path)


def test_discover_app_module_errors_on_multiple_src_candidates(tmp_path: Path) -> None:
    (tmp_path / "src" / "one").mkdir(parents=True)
    (tmp_path / "src" / "two").mkdir(parents=True)
    (tmp_path / "src" / "one" / "main.py").write_text("app = object()\n")
    (tmp_path / "src" / "two" / "main.py").write_text("app = object()\n")

    with pytest.raises(FlintError) as exc_info:
        discover_app_module(tmp_path)

    assert "multiple ASGI app candidates" in exc_info.value.message
