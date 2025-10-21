"""End-to-end tests that don't modify the project folder."""

import pytest
import tempfile
import subprocess
import sys
from pathlib import Path

from click.testing import CliRunner

from anvil.cli import main


class TestE2E:
    """End-to-end tests using isolated filesystems."""

    def test_new_lib_project_e2e(self):
        """Test creating a new lib project end-to-end."""
        runner = CliRunner()

        with runner.isolated_filesystem():
            # Create project
            result = runner.invoke(main, ["new", "testlib", "--profile", "lib"])
            assert result.exit_code == 0
            assert "Project 'testlib' created successfully" in result.output

            # Check directory structure
            assert Path("testlib").exists()
            assert Path("testlib/anvil.toml").exists()
            assert Path("testlib/pyproject.toml").exists()
            assert Path("testlib/src/testlib/__init__.py").exists()
            assert Path("testlib/tests/test_sanity.py").exists()

            # Check anvil.toml content
            anvil_content = Path("testlib/anvil.toml").read_text()
            assert "[project]" in anvil_content
            assert 'name = "testlib"' in anvil_content
            assert 'profile = "lib"' in anvil_content

            # Check pyproject.toml content
            pyproject_content = Path("testlib/pyproject.toml").read_text()
            assert "[project]" in pyproject_content
            assert 'name = "testlib"' in pyproject_content
            assert "[build-system]" in pyproject_content

            # Clean up created project
            import shutil

            if Path("testlib").exists():
                shutil.rmtree("testlib")

    def test_new_cli_project_e2e(self):
        """Test creating a new CLI project end-to-end."""
        runner = CliRunner()

        with runner.isolated_filesystem():
            result = runner.invoke(main, ["new", "testcli", "--profile", "cli"])
            assert result.exit_code == 0

            # Check CLI-specific files
            assert Path("testcli/src/testcli/__main__.py").exists()

            # Check pyproject.toml has scripts
            pyproject_content = Path("testcli/pyproject.toml").read_text()
            assert "[project.scripts]" in pyproject_content
            assert 'testcli = "testcli.__main__:main"' in pyproject_content

            # Clean up created project
            import shutil

            if Path("testcli").exists():
                shutil.rmtree("testcli")

    def test_new_api_project_fastapi_e2e(self):
        """Test creating a new FastAPI project end-to-end."""
        runner = CliRunner()

        with runner.isolated_filesystem():
            result = runner.invoke(
                main, ["new", "testapi", "--profile", "api", "--template", "fastapi"]
            )
            assert result.exit_code == 0

            # Check FastAPI-specific files
            assert Path("testapi/src/testapi/app.py").exists()
            assert Path("testapi/src/testapi/__main__.py").exists()

            # Check app.py content
            app_content = Path("testapi/src/testapi/app.py").read_text()
            assert "from fastapi import FastAPI" in app_content
            assert "app = FastAPI" in app_content
            assert '@app.get("/")' in app_content

            # Check __main__.py content
            main_content = Path("testapi/src/testapi/__main__.py").read_text()
            assert "import uvicorn" in main_content
            assert "uvicorn.run" in main_content

            # Check pyproject.toml dependencies
            pyproject_content = Path("testapi/pyproject.toml").read_text()
            assert "fastapi" in pyproject_content
            assert "uvicorn" in pyproject_content

            # Clean up created project
            import shutil

            if Path("testapi").exists():
                shutil.rmtree("testapi")

    def test_new_api_project_flask_e2e(self):
        """Test creating a new Flask project end-to-end."""
        runner = CliRunner()

        with runner.isolated_filesystem():
            result = runner.invoke(
                main, ["new", "testapi", "--profile", "api", "--template", "flask"]
            )
            assert result.exit_code == 0

            # Check app.py content
            app_content = Path("testapi/src/testapi/app.py").read_text()
            assert "from flask import Flask" in app_content
            assert '@app.route("/")' in app_content

            # Check pyproject.toml dependencies
            pyproject_content = Path("testapi/pyproject.toml").read_text()
            assert "flask" in pyproject_content

            # Clean up created project
            import shutil

            if Path("testapi").exists():
                shutil.rmtree("testapi")

    def test_invalid_profile_error(self):
        """Test error handling for invalid profile."""
        runner = CliRunner()

        with runner.isolated_filesystem():
            result = runner.invoke(main, ["new", "test", "--profile", "invalid"])
            assert result.exit_code == 0  # Click doesn't exit on print
            assert "Unknown profile 'invalid'" in result.output

    def test_duplicate_project_error(self):
        """Test error handling for duplicate project directory."""
        runner = CliRunner()

        with runner.isolated_filesystem():
            # Create directory first
            Path("testproject").mkdir()

            result = runner.invoke(main, ["new", "testproject", "--profile", "lib"])
            assert result.exit_code == 0  # Click doesn't exit on print
            assert "Directory 'testproject' already exists" in result.output

    def test_project_structure_integrity(self):
        """Test that all created files are syntactically valid."""
        runner = CliRunner()

        with runner.isolated_filesystem():
            runner.invoke(main, ["new", "testlib", "--profile", "lib"])

            # Check that Python files are syntactically valid
            python_files = [
                "testlib/src/testlib/__init__.py",
                "testlib/tests/test_sanity.py",
            ]

            for py_file in python_files:
                if Path(py_file).exists():
                    # Try to compile the file
                    with open(py_file, "r") as f:
                        content = f.read()
                    compile(content, py_file, "exec")

            # Clean up created project
            import shutil

            if Path("testlib").exists():
                shutil.rmtree("testlib")

    def test_anvil_toml_config_integrity(self):
        """Test that anvil.toml contains valid configuration."""
        runner = CliRunner()

        with runner.isolated_filesystem():
            runner.invoke(main, ["new", "testlib", "--profile", "lib"])

            # Should be able to load the config without errors
            import sys

            sys.path.insert(0, str(Path("testlib").absolute()))

            try:
                from anvil.config import Config

                config = Config(Path("testlib"))
                config.load()

                # Verify key values
                assert config.get("project.name") == "testlib"
                assert config.get("project.profile") == "lib"
                assert config.get("features.lint") is True

            finally:
                sys.path.remove(str(Path("testlib").absolute()))

            # Clean up created project
            import shutil

            if Path("testlib").exists():
                shutil.rmtree("testlib")
