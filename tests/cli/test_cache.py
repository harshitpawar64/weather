from unittest.mock import MagicMock

import pytest
from typer.testing import CliRunner

from weather.cache import Cache
from weather.cli import app


def test_path(runner: CliRunner) -> None:
    result = runner.invoke(app, ["cache", "path"])
    assert result.exit_code == 0
    assert "cache.bin" in result.stdout


def test_prune_clean(runner: CliRunner, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(Cache, "prune", lambda self: 0)
    result = runner.invoke(app, ["cache", "prune"])
    assert result.exit_code == 0
    assert "Cache is already clean" in result.stdout


def test_prune_with_entries(runner: CliRunner, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(Cache, "prune", lambda self: 3)
    result = runner.invoke(app, ["cache", "prune"])
    assert result.exit_code == 0
    assert "Pruned 3 expired cache entries" in result.stdout


def test_clear_success(runner: CliRunner, monkeypatch: pytest.MonkeyPatch) -> None:
    mock_clear = MagicMock()
    monkeypatch.setattr(Cache, "clear", mock_clear)
    result = runner.invoke(app, ["cache", "clear"])
    assert result.exit_code == 0
    assert "Cache cleared successfully" in result.stdout
    mock_clear.assert_called_once()


def test_clear_error(runner: CliRunner, monkeypatch: pytest.MonkeyPatch) -> None:
    mock_clear = MagicMock(side_effect=PermissionError("Permission denied"))
    monkeypatch.setattr(Cache, "clear", mock_clear)
    result = runner.invoke(app, ["cache", "clear"])
    assert result.exit_code == 1
    assert "Failed to clear cache: Permission denied" in result.stderr
