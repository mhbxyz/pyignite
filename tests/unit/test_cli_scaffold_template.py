from pathlib import Path

from pyqck.scaffold import CLITemplateContext, build_cli_template


def test_cli_template_builds_expected_layout() -> None:
    context = CLITemplateContext.from_project_name("My CLI")
    files = build_cli_template(context)

    assert Path("pyproject.toml") in files
    assert Path("pyquick.toml") in files
    assert Path("src/my_cli/__init__.py") in files
    assert Path("src/my_cli/main.py") in files
    assert Path("tests/test_my_cli.py") in files


def test_cli_template_uses_cli_profile_and_default_template() -> None:
    context = CLITemplateContext.from_project_name("billing-cli")
    files = build_cli_template(context)

    pyquick_toml = files[Path("pyquick.toml")]
    assert 'profile = "cli"' in pyquick_toml
    assert 'template = "baseline-cli"' in pyquick_toml
    assert 'running = "python"' in pyquick_toml


def test_cli_template_contains_script_entrypoint_and_quality_defaults() -> None:
    context = CLITemplateContext.from_project_name("billing-cli")
    files = build_cli_template(context)

    pyproject = files[Path("pyproject.toml")]
    assert "[project.scripts]" in pyproject
    assert 'billing_cli = "billing_cli.main:main"' in pyproject
    assert '"pytest>=8.3.0"' in pyproject
    assert '"ruff>=0.8.0"' in pyproject
    assert '"pyright>=1.1.390"' in pyproject


def test_cli_template_generates_callable_entrypoint_and_test() -> None:
    context = CLITemplateContext.from_project_name("billing-cli")
    files = build_cli_template(context)

    main_module = files[Path("src/billing_cli/main.py")]
    test_module = files[Path("tests/test_billing_cli.py")]
    assert "def main() -> int:" in main_module
    assert 'print("hello from pyqck cli profile")' in main_module
    assert "from billing_cli.main import main" in test_module
    assert "assert main() == 0" in test_module
