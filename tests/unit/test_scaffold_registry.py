from pathlib import Path

import pytest

from flint.scaffold.catalog import build_default_scaffold_registry
from flint.scaffold.registry import (
    DevMode,
    IncompatibleTemplateError,
    ProfileCapabilities,
    RunMode,
    ReservedProfileError,
    ScaffoldRegistry,
    UnknownProfileError,
    UnknownTemplateError,
)


def _files(project_name: str) -> dict[Path, str]:
    return {Path("README.md"): f"# {project_name}\n"}


def test_registry_resolves_default_template_and_builds_files() -> None:
    registry = ScaffoldRegistry()
    registry.register(
        profile="api",
        template="fastapi",
        generator=_files,
        capabilities=ProfileCapabilities(RunMode.SERVER, DevMode.SERVER_WITH_CHECKS),
        default=True,
    )

    selection = registry.build(project_name="myapi", profile="api")

    assert selection.profile == "api"
    assert selection.template == "fastapi"
    assert selection.files[Path("README.md")] == "# myapi\n"


def test_registry_rejects_unknown_profile() -> None:
    registry = ScaffoldRegistry()
    registry.register(
        profile="api",
        template="fastapi",
        generator=_files,
        capabilities=ProfileCapabilities(RunMode.SERVER, DevMode.SERVER_WITH_CHECKS),
        default=True,
    )

    with pytest.raises(UnknownProfileError):
        registry.build(project_name="demo", profile="worker")


def test_registry_rejects_unknown_template_for_profile() -> None:
    registry = ScaffoldRegistry()
    registry.register(
        profile="api",
        template="fastapi",
        generator=_files,
        capabilities=ProfileCapabilities(RunMode.SERVER, DevMode.SERVER_WITH_CHECKS),
        default=True,
    )

    with pytest.raises(UnknownTemplateError):
        registry.build(project_name="demo", profile="api", template="flask")


def test_registry_rejects_incompatible_template_pair() -> None:
    registry = ScaffoldRegistry()
    registry.register(
        profile="api",
        template="fastapi",
        generator=_files,
        capabilities=ProfileCapabilities(RunMode.SERVER, DevMode.SERVER_WITH_CHECKS),
        default=True,
    )
    registry.register(
        profile="cli",
        template="baseline-cli",
        generator=_files,
        capabilities=ProfileCapabilities(RunMode.CLI, DevMode.CHECKS_ONLY),
        default=True,
    )

    with pytest.raises(IncompatibleTemplateError):
        registry.build(project_name="demo", profile="cli", template="fastapi")


def test_default_registry_resolves_lib_profile() -> None:
    registry = build_default_scaffold_registry()

    selection = registry.build(project_name="mylib", profile="lib")

    assert selection.profile == "lib"
    assert selection.template == "baseline-lib"
    assert Path("pyproject.toml") in selection.files


def test_default_registry_resolves_cli_profile() -> None:
    registry = build_default_scaffold_registry()

    selection = registry.build(project_name="mycli", profile="cli")

    assert selection.profile == "cli"
    assert selection.template == "baseline-cli"
    assert Path("src/mycli/main.py") in selection.files


def test_default_registry_marks_web_as_reserved_profile() -> None:
    registry = build_default_scaffold_registry()

    with pytest.raises(ReservedProfileError):
        registry.build(project_name="demo", profile="web")


def test_default_registry_exposes_profile_capabilities() -> None:
    registry = build_default_scaffold_registry()

    api = registry.capabilities_for(profile="api", template="fastapi")
    cli = registry.capabilities_for(profile="cli", template="baseline-cli")
    lib = registry.capabilities_for(profile="lib", template="baseline-lib")

    assert api == ProfileCapabilities(RunMode.SERVER, DevMode.SERVER_WITH_CHECKS)
    assert cli == ProfileCapabilities(RunMode.CLI, DevMode.CHECKS_ONLY)
    assert lib == ProfileCapabilities(RunMode.UNSUPPORTED, DevMode.CHECKS_ONLY)


def test_default_registry_lists_scaffoldable_profiles_and_templates() -> None:
    registry = build_default_scaffold_registry()

    assert registry.scaffoldable_profiles() == ("api", "cli", "lib")
    assert registry.templates_for("api") == ("fastapi",)
    assert registry.default_template_for("cli") == "baseline-cli"
