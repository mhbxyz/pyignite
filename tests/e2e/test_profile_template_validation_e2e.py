from __future__ import annotations

from pathlib import Path
import sys
import subprocess

from tests.e2e.helpers import run_flint
from tests.e2e.helpers import env_with_repo_src


def test_new_rejects_unknown_profile(tmp_path: Path) -> None:
    result = run_flint(["new", "bad", "--profile", "worker"], cwd=tmp_path)

    assert result.returncode == 2
    assert "ERROR [usage] Unsupported profile `worker`." in result.stderr
    assert "Hint:" in result.stderr


def test_new_rejects_reserved_profile(tmp_path: Path) -> None:
    result = run_flint(["new", "bad", "--profile", "web"], cwd=tmp_path)

    assert result.returncode == 2
    assert "ERROR [usage] Profile `web` is reserved and not scaffoldable yet." in result.stderr
    assert "Hint:" in result.stderr


def test_new_rejects_unknown_template(tmp_path: Path) -> None:
    result = run_flint(
        ["new", "bad", "--profile", "api", "--template", "flask"],
        cwd=tmp_path,
    )

    assert result.returncode == 2
    assert "ERROR [usage] Unsupported template `flask` for profile `api`." in result.stderr
    assert "Hint:" in result.stderr


def test_new_rejects_incompatible_profile_template_pair(tmp_path: Path) -> None:
    result = run_flint(
        ["new", "bad", "--profile", "api", "--template", "baseline-cli"],
        cwd=tmp_path,
    )

    assert result.returncode == 2
    assert (
        "ERROR [usage] Template `baseline-cli` is not compatible with profile `api`."
        in result.stderr
    )
    assert "Hint:" in result.stderr


def test_new_interactive_cancel_does_not_create_project(tmp_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "flint", "new"],
        cwd=tmp_path,
        env=env_with_repo_src(),
        input="demo\napi\nn\n",
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Cancelled." in result.stdout
    assert not (tmp_path / "demo").exists()
