from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from flint.cli import app
from tests.helpers import copy_fixture

runner = CliRunner()


def test_check_command_exits_zero_on_success(tmp_path: Path) -> None:
    (tmp_path / "src" / "demo").mkdir(parents=True)
    (tmp_path / "src" / "demo" / "main.py").write_text("app = object()\n")

    with patch("flint.cli.run_check_pipeline", return_value=0):
        result = runner.invoke(app, ["check", "--cwd", str(tmp_path)])

    assert result.exit_code == 0


def test_run_command_renders_actionable_config_error(tmp_path: Path) -> None:
    result = runner.invoke(app, ["run", "--cwd", str(tmp_path)])

    assert result.exit_code == 2
    assert "ERROR [config] Could not resolve an ASGI app target." in result.stderr
    assert "Hint:" in result.stderr


def test_check_command_uses_canonical_sample_repo(tmp_path: Path) -> None:
    project = copy_fixture(tmp_path, "fastapi_sample")

    with patch("flint.tools.ensure_uv_available"), patch("flint.tools.run_step", return_value=0):
        result = runner.invoke(app, ["check", "--cwd", str(project)])

    assert result.exit_code == 0
    assert "==> lint" in result.stdout
    assert "OK test" in result.stdout


def test_run_command_uses_config_override_module(tmp_path: Path) -> None:
    project = copy_fixture(tmp_path, "fastapi_sample")
    (project / "flint.toml").write_text('[app]\nmodule = "demo_api.main:app"\n')

    with patch("flint.tools.ensure_uv_available"), patch("flint.tools.subprocess.run") as run_mock:
        run_mock.return_value.returncode = 0
        result = runner.invoke(app, ["run", "--cwd", str(project)])

    assert result.exit_code == 0
    command = run_mock.call_args.args[0]
    assert command[:4] == ["uv", "run", "uvicorn", "demo_api.main:app"]
