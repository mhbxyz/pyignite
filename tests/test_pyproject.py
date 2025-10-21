"""Tests for pyproject.toml generation."""

import tempfile
from pathlib import Path

from anvil.config import Config
from anvil.pyproject import PyProjectGenerator


class TestPyProjectGenerator:
    """Test PyProjectGenerator functionality."""

    def test_generate_lib_profile(self):
        """Test pyproject.toml generation for library profile."""
        config = Config()
        config.set("project.name", "testlib")
        config.set("project.package", "testlib")
        config.set("project.profile", "lib")
        config.set("project.python", "3.11")

        generator = PyProjectGenerator(config)
        pyproject = generator.generate()

        # Check basic structure
        assert pyproject["project"]["name"] == "testlib"
        assert pyproject["project"]["version"] == "0.1.0"
        assert ">=3.11" in pyproject["project"]["requires-python"]

        # Check build system
        assert pyproject["build-system"]["requires"] == ["hatchling"]
        assert pyproject["build-system"]["build-backend"] == "hatchling.build"

        # Check optional dependencies for lib
        assert "dev" in pyproject["project"]["optional-dependencies"]
        dev_deps = pyproject["project"]["optional-dependencies"]["dev"]
        assert "pytest>=7.0.0" in dev_deps
        assert "ruff>=0.1.0" in dev_deps

        # Check tool configurations
        assert "tool" in pyproject
        assert "ruff" in pyproject["tool"]
        assert "pytest" in pyproject["tool"]

    def test_generate_cli_profile(self):
        """Test pyproject.toml generation for CLI profile."""
        config = Config()
        config.set("project.name", "testcli")
        config.set("project.package", "testcli")
        config.set("project.profile", "cli")

        generator = PyProjectGenerator(config)
        pyproject = generator.generate()

        # Check scripts
        assert "scripts" in pyproject["project"]
        assert "testcli" in pyproject["project"]["scripts"]
        assert "testcli.__main__:main" in pyproject["project"]["scripts"]["testcli"]

    def test_generate_api_profile_fastapi(self):
        """Test pyproject.toml generation for API profile with FastAPI."""
        config = Config()
        config.set("project.name", "testapi")
        config.set("project.package", "testapi")
        config.set("project.profile", "api")
        config.set("api.template", "fastapi")

        generator = PyProjectGenerator(config)
        pyproject = generator.generate()

        # Check dependencies
        deps = pyproject["project"]["dependencies"]
        assert any("fastapi" in dep for dep in deps)
        assert any("uvicorn" in dep for dep in deps)

        # Check scripts
        scripts = pyproject["project"]["scripts"]
        assert "testapi" in scripts
        assert "uvicorn" in scripts["testapi"]

    def test_generate_api_profile_flask(self):
        """Test pyproject.toml generation for API profile with Flask."""
        config = Config()
        config.set("project.name", "testapi")
        config.set("project.package", "testapi")
        config.set("project.profile", "api")
        config.set("api.template", "flask")

        generator = PyProjectGenerator(config)
        pyproject = generator.generate()

        # Check dependencies
        deps = pyproject["project"]["dependencies"]
        assert any("flask" in dep for dep in deps)

        # Check scripts
        scripts = pyproject["project"]["scripts"]
        assert "flask" in scripts["testapi"]

    def test_write_to_file(self):
        """Test writing pyproject.toml to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = Config()
            config.set("project.name", "testlib")
            config.set("project.profile", "lib")

            generator = PyProjectGenerator(config)
            pyproject_path = Path(tmpdir) / "pyproject.toml"
            generator.write_to_file(pyproject_path)

            # Check file exists and has content
            assert pyproject_path.exists()
            content = pyproject_path.read_text()
            assert "[project]" in content
            assert 'name = "testlib"' in content
            assert "[build-system]" in content

    def test_dict_to_toml_basic(self):
        """Test basic TOML conversion."""
        config = Config()
        config.set("project.name", "test")

        generator = PyProjectGenerator(config)
        pyproject = generator.generate()

        # This tests the internal _dict_to_toml method indirectly
        toml_str = generator._dict_to_toml(pyproject)
        assert isinstance(toml_str, str)
        assert "[project]" in toml_str
        assert "[build-system]" in toml_str
