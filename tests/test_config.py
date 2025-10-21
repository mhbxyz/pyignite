"""Tests for configuration management."""

import tempfile
from pathlib import Path

from anvil.config import Config


class TestConfig:
    """Test Config class functionality."""

    def test_config_initialization(self):
        """Test config initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = Config(Path(tmpdir))
            assert config.project_root == Path(tmpdir)

    def test_config_get_set(self):
        """Test basic get/set operations."""
        config = Config()

        # Test setting and getting values
        config.set("project.name", "testproject")
        assert config.get("project.name") == "testproject"

        # Test nested keys
        config.set("tooling.runner", "uv")
        assert config.get("tooling.runner") == "uv"

        # Test default values
        assert config.get("nonexistent.key", "default") == "default"

    def test_config_load_save(self):
        """Test loading and saving configuration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "anvil.toml"
            config = Config(Path(tmpdir))

            # Set some values
            config.set("project.name", "testproject")
            config.set("project.profile", "lib")
            config.set("features.lint", True)

            # Save config
            config.save()

            # Verify file exists
            assert config_file.exists()

            # Load config in new instance
            new_config = Config(Path(tmpdir))
            new_config.load()

            # Verify values
            assert new_config.get("project.name") == "testproject"
            assert new_config.get("project.profile") == "lib"
            assert new_config.get("features.lint") is True

    def test_config_default_values(self):
        """Test default configuration values."""
        config = Config()

        # Load defaults (no file exists)
        config.load()

        assert config.get("project.name") == "myproject"
        assert config.get("project.python") == "3.11"
        assert config.get("tooling.runner") == "uv"
        assert config.get("features.lint") is True

    def test_config_nested_dict_creation(self):
        """Test that setting nested keys creates intermediate dicts."""
        config = Config()

        config.set("deeply.nested.key", "value")
        assert config.get("deeply.nested.key") == "value"
        assert isinstance(config.get("deeply.nested"), dict)
        assert isinstance(config.get("deeply"), dict)
