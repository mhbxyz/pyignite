"""Tests for profile definitions and scaffolding."""

import pytest
import tempfile
from pathlib import Path

from anvil.config import Config
from anvil.profiles import (
    LibProfile,
    CliProfile,
    ApiProfile,
    ServiceProfile,
    MonorepoProfile,
    get_profile,
    list_profiles,
)


class TestProfiles:
    """Test profile functionality."""

    def test_list_profiles(self):
        """Test listing available profiles."""
        profiles = list_profiles()
        expected = ["lib", "cli", "api", "service", "monorepo"]
        assert set(profiles) == set(expected)

    def test_get_profile(self):
        """Test getting profile instances."""
        profile = get_profile("lib")
        assert isinstance(profile, LibProfile)
        assert profile.name == "lib"

        # Test invalid profile
        assert get_profile("invalid") is None

    def test_lib_profile_scaffold(self):
        """Test library profile scaffolding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = Config(Path(tmpdir))
            config.set("project.package", "testlib")

            profile = LibProfile()
            profile.scaffold("testlib", config)

            # Check directory structure
            assert (Path(tmpdir) / "src" / "testlib" / "__init__.py").exists()
            assert (Path(tmpdir) / "tests" / "__init__.py").exists()
            assert (Path(tmpdir) / "tests" / "test_sanity.py").exists()

            # Check __init__.py content
            init_file = Path(tmpdir) / "src" / "testlib" / "__init__.py"
            content = init_file.read_text()
            assert '"""Package testlib."""' in content
            assert '__version__ = "0.1.0"' in content

    def test_cli_profile_scaffold(self):
        """Test CLI profile scaffolding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = Config(Path(tmpdir))
            config.set("project.package", "testcli")

            profile = CliProfile()
            profile.scaffold("testcli", config)

            # Check directory structure
            assert (Path(tmpdir) / "src" / "testcli" / "__init__.py").exists()
            assert (Path(tmpdir) / "src" / "testcli" / "__main__.py").exists()

            # Check __main__.py content
            main_file = Path(tmpdir) / "src" / "testcli" / "__main__.py"
            content = main_file.read_text()
            assert "def main():" in content
            assert "Hello from testcli" in content

    def test_api_profile_scaffold_fastapi(self):
        """Test API profile scaffolding with FastAPI template."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = Config(Path(tmpdir))
            config.set("project.package", "testapi")
            config.set("api.template", "fastapi")

            profile = ApiProfile()
            profile.scaffold("testapi", config)

            # Check directory structure
            assert (Path(tmpdir) / "src" / "testapi" / "__init__.py").exists()
            assert (Path(tmpdir) / "src" / "testapi" / "app.py").exists()
            assert (Path(tmpdir) / "src" / "testapi" / "__main__.py").exists()

            # Check app.py content
            app_file = Path(tmpdir) / "src" / "testapi" / "app.py"
            content = app_file.read_text()
            assert "from fastapi import FastAPI" in content
            assert "app = FastAPI" in content
            assert '@app.get("/")' in content
            assert '@app.get("/health")' in content

            # Check __main__.py content
            main_file = Path(tmpdir) / "src" / "testapi" / "__main__.py"
            content = main_file.read_text()
            assert "import uvicorn" in content
            assert "uvicorn.run" in content

    def test_api_profile_scaffold_flask(self):
        """Test API profile scaffolding with Flask template."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = Config(Path(tmpdir))
            config.set("project.package", "testapi")
            config.set("api.template", "flask")

            profile = ApiProfile()
            profile.scaffold("testapi", config)

            # Check app.py content
            app_file = Path(tmpdir) / "src" / "testapi" / "app.py"
            content = app_file.read_text()
            assert "from flask import Flask" in content
            assert "app = Flask" in content
            assert '@app.route("/")' in content

    def test_api_profile_scaffold_default(self):
        """Test API profile scaffolding with default template."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = Config(Path(tmpdir))
            config.set("project.package", "testapi")
            # No template specified

            profile = ApiProfile()
            profile.scaffold("testapi", config)

            # Check basic structure
            app_file = Path(tmpdir) / "src" / "testapi" / "app.py"
            content = app_file.read_text()
            assert "# Placeholder for app" in content

    def test_service_profile_scaffold(self):
        """Test service profile scaffolding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = Config(Path(tmpdir))
            config.set("project.package", "testservice")

            profile = ServiceProfile()
            profile.scaffold("testservice", config)

            # Check directory structure
            assert (Path(tmpdir) / "src" / "testservice" / "__init__.py").exists()
            assert (Path(tmpdir) / "src" / "testservice" / "service.py").exists()

            # Check service.py content
            service_file = Path(tmpdir) / "src" / "testservice" / "service.py"
            content = service_file.read_text()
            assert "def main():" in content
            assert "Service testservice starting" in content

    def test_monorepo_profile_scaffold(self):
        """Test monorepo profile scaffolding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = Config(Path(tmpdir))

            profile = MonorepoProfile()
            profile.scaffold("testmonorepo", config)

            # Check directory structure
            assert (Path(tmpdir) / "packages").exists()
            assert (Path(tmpdir) / "packages" / "README.md").exists()

            # Check README content
            readme_file = Path(tmpdir) / "packages" / "README.md"
            content = readme_file.read_text()
            assert "# Packages" in content
