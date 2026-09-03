from unittest.mock import MagicMock

import pytest
from typer.testing import CliRunner

from weather.cache import Cache, CacheStats
from weather.cli import app


def test_path(runner: CliRunner) -> None:
    result = runner.invoke(app, ["cache", "path"])
    assert result.exit_code == 0
    assert "cache.bin" in result.stdout


def test_stats_clean(runner: CliRunner, monkeypatch: pytest.MonkeyPatch) -> None:
    mock_stats = CacheStats(size=1400, queries=3, entries=2, expired=0)
    monkeypatch.setattr(Cache, "stats", lambda self: mock_stats)
    result = runner.invoke(app, ["cache", "stats"])
    assert result.exit_code == 0
    assert "Size:" in result.stdout
    assert "1.4 KB" in result.stdout
    assert "Queries:" in result.stdout
    assert "3" in result.stdout
    assert "Entries:" in result.stdout
    assert "2" in result.stdout
    assert "Expired:" in result.stdout
    assert "0" in result.stdout
    assert "clean" in result.stdout


def test_stats_with_expired(runner: CliRunner, monkeypatch: pytest.MonkeyPatch) -> None:
    mock_stats = CacheStats(size=2048, queries=5, entries=4, expired=2)
    monkeypatch.setattr(Cache, "stats", lambda self: mock_stats)
    result = runner.invoke(app, ["cache", "stats"])
    assert result.exit_code == 0
    assert "2.0 KB" in result.stdout
    assert "run 'weather cache prune' to clean" in result.stdout


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
