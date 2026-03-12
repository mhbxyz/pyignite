from pathlib import Path

from typer.testing import CliRunner

from flint.cli import app


def test_new_generates_fastapi_project_structure() -> None:
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(
            app,
            ["new", "my-api", "--profile", "api", "--template", "fastapi"],
        )

        assert result.exit_code == 0
        assert "Created project `my-api`" in result.output
        assert "flint run" in result.output

        project_dir = Path("my-api")
        assert (project_dir / "flint.toml").exists()
        assert (project_dir / "src" / "my_api" / "main.py").exists()
        assert (project_dir / "src" / "my_api" / "api" / "health.py").exists()
        assert (project_dir / "tests" / "test_health.py").exists()

        flint_toml = (project_dir / "flint.toml").read_text(encoding="utf-8")
        assert 'app = "my_api.main:app"' in flint_toml


def test_new_interactive_generates_project_structure() -> None:
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(
            app,
            ["new"],
            input="my-interactive\napi\ny\n",
        )

        assert result.exit_code == 0
        assert "Project summary:" in result.output
        assert "Created project `my-interactive`" in result.output

        project_dir = Path("my-interactive")
        assert (project_dir / "flint.toml").exists()
        assert (project_dir / "src" / "my_interactive" / "main.py").exists()


def test_new_interactive_reprompts_invalid_values_and_can_cancel() -> None:
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(
            app,
            ["new"],
            input="\nmy-lib\nworker\nlib\nn\n",
        )

        assert result.exit_code == 0
        assert result.output.count("Project name:") == 2
        assert "Unsupported profile `worker`." in result.output
        assert "Cancelled." in result.output
        assert not Path("my-lib").exists()


def test_new_generates_lib_project_structure() -> None:
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(app, ["new", "my-lib", "--profile", "lib"])

        assert result.exit_code == 0
        assert (
            "Created project `my-lib` with profile `lib` and template `baseline-lib`."
            in result.output
        )

        project_dir = Path("my-lib")
        assert (project_dir / "pyproject.toml").exists()
        assert (project_dir / "flint.toml").exists()
        assert (project_dir / "src" / "my_lib" / "__init__.py").exists()
        assert (project_dir / "tests" / "test_my_lib.py").exists()


def test_new_generates_cli_project_structure() -> None:
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(app, ["new", "my-cli", "--profile", "cli"])

        assert result.exit_code == 0
        assert (
            "Created project `my-cli` with profile `cli` and template `baseline-cli`."
            in result.output
        )

        project_dir = Path("my-cli")
        assert (project_dir / "pyproject.toml").exists()
        assert (project_dir / "flint.toml").exists()
        assert (project_dir / "src" / "my_cli" / "main.py").exists()
        assert (project_dir / "tests" / "test_my_cli.py").exists()


def test_new_rejects_non_empty_destination() -> None:
    runner = CliRunner()

    with runner.isolated_filesystem():
        project_dir = Path("myapi")
        project_dir.mkdir()
        (project_dir / "existing.txt").write_text("hello", encoding="utf-8")

        result = runner.invoke(app, ["new", "myapi", "--profile", "api", "--template", "fastapi"])

        assert result.exit_code == 2
        assert "ERROR [usage] Destination `myapi` already exists and is not empty." in result.output


def test_new_rejects_invalid_profile_or_template() -> None:
    runner = CliRunner()

    with runner.isolated_filesystem():
        invalid_profile = runner.invoke(app, ["new", "myapi", "--profile", "worker"])
        assert invalid_profile.exit_code == 2
        assert "ERROR [usage] Unsupported profile `worker`." in invalid_profile.output

        invalid_template = runner.invoke(app, ["new", "myapi", "--template", "flask"])
        assert invalid_template.exit_code == 2
        assert (
            "ERROR [usage] Unsupported template `flask` for profile `api`."
            in invalid_template.output
        )


def test_new_rejects_incompatible_profile_template_pair() -> None:
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(
            app, ["new", "mycli", "--profile", "api", "--template", "baseline-lib"]
        )

        assert result.exit_code == 2
        assert (
            "ERROR [usage] Template `baseline-lib` is not compatible with profile `api`."
            in result.output
        )
