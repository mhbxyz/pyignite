"""Main CLI entry point for Anvil."""

import sys
from typing import Optional

import click
from rich.console import Console

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def main() -> None:
    """Anvil: Python toolchain orchestrator.

    Scaffold, configure, and orchestrate Python projects with consistent tooling.
    """
    pass


@main.command()
def new() -> None:
    """Scaffold a new Python project."""
    console.print("[bold green]🚀[/bold green] Creating new project...")
    console.print("[yellow]Not implemented yet[/yellow]")


@main.command()
def dev() -> None:
    """Run project in development mode with watch."""
    console.print("[bold blue]👀[/bold blue] Starting development mode...")
    console.print("[yellow]Not implemented yet[/yellow]")


@main.command()
def run() -> None:
    """Run the canonical executable for the project."""
    console.print("[bold purple]▶️[/bold purple] Running project...")
    console.print("[yellow]Not implemented yet[/yellow]")


@main.command()
def fmt() -> None:
    """Format code using ruff."""
    console.print("[bold cyan]🎨[/bold cyan] Formatting code...")
    console.print("[yellow]Not implemented yet[/yellow]")


@main.command()
def lint() -> None:
    """Lint code using ruff."""
    console.print("[bold orange]🔍[/bold orange] Linting code...")
    console.print("[yellow]Not implemented yet[/yellow]")


@main.command()
def test() -> None:
    """Run tests using pytest."""
    console.print("[bold green]🧪[/bold green] Running tests...")
    console.print("[yellow]Not implemented yet[/yellow]")


@main.command()
def build() -> None:
    """Build the project using uv."""
    console.print("[bold magenta]📦[/bold magenta] Building project...")
    console.print("[yellow]Not implemented yet[/yellow]")


if __name__ == "__main__":
    main()