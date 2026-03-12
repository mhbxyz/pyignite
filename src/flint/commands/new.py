from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import typer

from flint.scaffold import (
    ScaffoldLookupError,
    ScaffoldRegistry,
    build_default_scaffold_registry,
    normalize_package_name,
)
from flint.scaffold.writer import write_scaffold


@dataclass(slots=True, frozen=True)
class NewProjectAnswers:
    name: str
    profile: str
    template: str


def new_command(
    name: str | None = typer.Argument(None, help="Project directory name."),
    profile: str = typer.Option("api", "--profile", help="Project profile."),
    template: str | None = typer.Option(None, "--template", help="Template to use."),
) -> None:
    """Create a new Flint project scaffold."""

    registry = build_default_scaffold_registry()
    if name is None:
        answers = _prompt_for_new_project(registry)
        name = answers.name
        profile = answers.profile
        template = answers.template

    try:
        selection = registry.build(project_name=name, profile=profile, template=template)
    except ScaffoldLookupError as exc:
        _usage_error(exc.message, exc.hint)

    destination = Path.cwd() / name
    if destination.exists() and not destination.is_dir():
        _usage_error(
            f"Destination `{destination.name}` exists and is not a directory.",
            "Choose a different project name.",
        )
    if destination.exists() and any(destination.iterdir()):
        _usage_error(
            f"Destination `{destination.name}` already exists and is not empty.",
            "Choose a new directory name or empty the destination first.",
        )

    files = selection.files

    try:
        destination.mkdir(parents=True, exist_ok=True)
        write_scaffold(destination=destination, files=files)
    except OSError as exc:
        typer.secho(
            f"ERROR [tooling] Could not generate project `{name}`.",
            fg=typer.colors.RED,
            err=True,
        )
        typer.secho(
            f"Hint: Check filesystem permissions and free space ({exc}).",
            fg=typer.colors.YELLOW,
            err=True,
        )
        raise typer.Exit(code=1) from exc

    typer.secho(
        (
            f"Created project `{name}` with profile `{selection.profile}` "
            f"and template `{selection.template}`."
        ),
        fg=typer.colors.GREEN,
    )
    typer.echo("Next steps:")
    typer.echo(f"  cd {name}")
    typer.echo("  flint install")
    typer.echo("  flint run")
    typer.echo("  flint test")


def _prompt_for_new_project(registry: ScaffoldRegistry) -> NewProjectAnswers:
    project_name = _prompt_for_project_name()
    profile = _prompt_for_profile(registry)
    template = _prompt_for_template(registry, profile=profile)

    typer.echo("Project summary:")
    typer.echo(f"  name: {project_name}")
    typer.echo(f"  profile: {profile}")
    typer.echo(f"  template: {template}")
    typer.echo(f"  package: {normalize_package_name(project_name)}")
    typer.echo(f"  destination: {Path.cwd() / project_name}")

    confirmed = typer.confirm("Create project with these settings?", default=True)
    if not confirmed:
        typer.echo("Cancelled.")
        raise typer.Exit(code=0)

    return NewProjectAnswers(name=project_name, profile=profile, template=template)


def _prompt_for_project_name() -> str:
    while True:
        name = typer.prompt("Project name").strip()
        if name:
            return name
        typer.secho("Project name cannot be empty.", fg=typer.colors.RED, err=True)


def _prompt_for_profile(registry: ScaffoldRegistry) -> str:
    profiles = registry.scaffoldable_profiles()
    profile_choices = "/".join(profiles)
    while True:
        profile = typer.prompt(f"Profile [{profile_choices}]", default="api").strip()
        if profile in profiles:
            return profile
        typer.secho(
            f"Unsupported profile `{profile}`. Choose one of: {', '.join(profiles)}.",
            fg=typer.colors.RED,
            err=True,
        )


def _prompt_for_template(registry: ScaffoldRegistry, *, profile: str) -> str:
    templates = registry.templates_for(profile)
    default_template = registry.default_template_for(profile)
    if len(templates) == 1:
        return default_template

    template_choices = "/".join(templates)
    while True:
        template = typer.prompt(
            f"Template [{template_choices}]",
            default=default_template,
        ).strip()
        if template in templates:
            return template
        typer.secho(
            f"Unsupported template `{template}` for profile `{profile}`.",
            fg=typer.colors.RED,
            err=True,
        )


def _usage_error(message: str, hint: str) -> None:
    typer.secho(f"ERROR [usage] {message}", fg=typer.colors.RED, err=True)
    typer.secho(f"Hint: {hint}", fg=typer.colors.YELLOW, err=True)
    raise typer.Exit(code=2)
