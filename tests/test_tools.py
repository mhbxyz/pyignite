"""Tests for tool detection and execution."""

import pytest
from unittest.mock import patch, MagicMock

from anvil.config import Config
from anvil.tools import ToolDetector, ToolExecutor


class TestToolDetector:
    """Test ToolDetector functionality."""

    def test_tool_detection(self):
        """Test tool availability detection."""
        detector = ToolDetector()

        # Test with a tool that should exist (python)
        assert detector.is_available("python")

        # Test caching
        first_call = detector.is_available("python")
        second_call = detector.is_available("python")
        assert first_call == second_call

    def test_get_available_tools(self):
        """Test getting list of available tools."""
        detector = ToolDetector()

        # Test with tools that should exist
        tools = ["python", "pip"]
        available = detector.get_available_tools(tools)

        # Should return a subset of the input tools
        assert all(tool in tools for tool in available)
        assert isinstance(available, list)


class TestToolExecutor:
    """Test ToolExecutor functionality."""

    def test_executor_initialization(self):
        """Test executor initialization."""
        config = Config()
        executor = ToolExecutor(config)

        assert executor.config == config
        assert hasattr(executor, "detector")

    @patch("anvil.tools.subprocess.run")
    def test_run_command_success(self, mock_run):
        """Test successful command execution."""
        mock_run.return_value = MagicMock(returncode=0)

        config = Config()
        executor = ToolExecutor(config)

        result = executor.run_command(["echo", "test"])
        assert result == 0
        mock_run.assert_called_once()

    @patch("anvil.tools.subprocess.run")
    def test_run_command_failure(self, mock_run):
        """Test failed command execution."""
        mock_run.return_value = MagicMock(returncode=1)

        config = Config()
        executor = ToolExecutor(config)

        result = executor.run_command(["false"])
        assert result == 1

    @patch("anvil.tools.ToolExecutor.run_command")
    def test_run_ruff_check_available(self, mock_run_cmd):
        """Test ruff check when ruff is available."""
        mock_run_cmd.return_value = 0

        config = Config()
        executor = ToolExecutor(config)

        with patch.object(executor.detector, "is_available", return_value=True):
            result = executor.run_ruff_check(["src"])
            assert result == 0
            mock_run_cmd.assert_called_with(["ruff", "check", "src"])

    @patch("anvil.tools.ToolExecutor.run_command")
    def test_run_ruff_check_fallback(self, mock_run_cmd):
        """Test ruff check fallback when ruff is not available."""
        mock_run_cmd.return_value = 0

        config = Config()
        executor = ToolExecutor(config)

        with patch.object(executor.detector, "is_available", side_effect=[False, True]):
            result = executor.run_ruff_check(["src"])
            assert result == 0
            mock_run_cmd.assert_called_with(["flake8", "src"])

    @patch("anvil.tools.ToolExecutor.run_command")
    def test_run_pytest_available(self, mock_run_cmd):
        """Test pytest execution when available."""
        mock_run_cmd.return_value = 0

        config = Config()
        executor = ToolExecutor(config)

        with patch.object(executor.detector, "is_available", return_value=True):
            result = executor.run_pytest()
            assert result == 0
            mock_run_cmd.assert_called_with(["pytest"])

    @patch("anvil.tools.ToolExecutor.run_command")
    def test_run_pytest_unavailable(self, mock_run_cmd):
        """Test pytest execution when not available."""
        config = Config()
        executor = ToolExecutor(config)

        with patch.object(executor.detector, "is_available", return_value=False):
            result = executor.run_pytest()
            assert result == 1
            mock_run_cmd.assert_not_called()

    @patch("anvil.tools.ToolExecutor.run_command")
    def test_run_type_check_mypy(self, mock_run_cmd):
        """Test type checking with mypy preference."""
        mock_run_cmd.return_value = 0

        config = Config()
        config.set("features.types", "mypy")
        executor = ToolExecutor(config)

        with patch.object(executor.detector, "is_available", return_value=True):
            result = executor.run_type_check()
            assert result == 0
            # Should call mypy with paths
            assert mock_run_cmd.call_count >= 1

    @patch("anvil.tools.ToolExecutor.run_command")
    def test_run_type_check_pyright(self, mock_run_cmd):
        """Test type checking with pyright preference."""
        mock_run_cmd.return_value = 0

        config = Config()
        config.set("features.types", "pyright")
        executor = ToolExecutor(config)

        with patch.object(executor.detector, "is_available", return_value=True):
            result = executor.run_type_check()
            assert result == 0
            mock_run_cmd.assert_called_with(["pyright"])

    @patch("anvil.tools.ToolExecutor.run_command")
    def test_run_uv_build_with_uv(self, mock_run_cmd):
        """Test uv build when uv is available."""
        mock_run_cmd.return_value = 0

        config = Config()
        executor = ToolExecutor(config)

        with patch.object(executor.detector, "is_available", return_value=True):
            result = executor.run_uv_build(wheel=True, sdist=True)
            assert result == 0
            mock_run_cmd.assert_called_with(["uv", "build"])

    @patch("anvil.tools.ToolExecutor.run_command")
    def test_run_uv_build_fallback(self, mock_run_cmd):
        """Test uv build fallback when uv is not available."""
        mock_run_cmd.return_value = 0

        config = Config()
        executor = ToolExecutor(config)

        with patch.object(executor.detector, "is_available", side_effect=[False, True]):
            result = executor.run_uv_build()
            assert result == 0
            mock_run_cmd.assert_called_with(["python", "-m", "build"])
