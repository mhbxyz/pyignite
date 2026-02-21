from __future__ import annotations

from pathlib import Path

from pyqck.scaffold.cli_template import CLITemplateContext, build_cli_template
from pyqck.scaffold.fastapi import FastAPITemplateContext, build_fastapi_template
from pyqck.scaffold.lib_template import LibTemplateContext, build_lib_template
from pyqck.scaffold.registry import ScaffoldRegistry


def build_default_scaffold_registry() -> ScaffoldRegistry:
    registry = ScaffoldRegistry()
    registry.register(
        profile="api",
        template="fastapi",
        generator=_build_api_fastapi,
        default=True,
    )
    registry.register(
        profile="lib",
        template="baseline-lib",
        generator=_build_lib_baseline,
        default=True,
    )
    registry.register(
        profile="cli",
        template="baseline-cli",
        generator=_build_cli_baseline,
        default=True,
    )

    registry.reserve_profile("web")
    registry.reserve_profile("game")
    return registry


def _build_api_fastapi(project_name: str) -> dict[Path, str]:
    context = FastAPITemplateContext.from_project_name(project_name)
    return build_fastapi_template(context)


def _build_lib_baseline(project_name: str) -> dict[Path, str]:
    context = LibTemplateContext.from_project_name(project_name)
    return build_lib_template(context)


def _build_cli_baseline(project_name: str) -> dict[Path, str]:
    context = CLITemplateContext.from_project_name(project_name)
    return build_cli_template(context)
