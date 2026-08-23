import importlib
import runpy
from unittest.mock import AsyncMock, MagicMock

import pytest
from typer.testing import CliRunner

import tests.constants as c
from weather.cli import app
from weather.exceptions import ServiceError
from weather.models import Theme, UnitSystem


def test_version(runner: CliRunner) -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "weather" in result.stdout


def test_conflicting_units(runner: CliRunner) -> None:
    result = runner.invoke(app, ["--metric", "--imperial"])
    assert result.exit_code == 2
    assert "Cannot use both" in result.stderr


def test_success_metric(runner: CliRunner, monkeypatch: pytest.MonkeyPatch) -> None:
    mock_run = AsyncMock()
    monkeypatch.setattr("weather.app.run", mock_run)
    result = runner.invoke(app, ["-l", c.QUERY, "-d", "3", "--metric", "--json", "-v"])
    assert result.exit_code == 0
    mock_run.assert_awaited_once_with(c.QUERY, UnitSystem.METRIC, None, 3, True)


def test_success_imperial_and_theme(
    runner: CliRunner, monkeypatch: pytest.MonkeyPatch
) -> None:
    mock_run = AsyncMock()
    monkeypatch.setattr("weather.app.run", mock_run)
    result = runner.invoke(app, ["-l", c.QUERY, "--imperial", "-t", "default"])
    assert result.exit_code == 0
    mock_run.assert_awaited_once_with(
        c.QUERY, UnitSystem.IMPERIAL, Theme.DEFAULT, 7, False
    )


def test_weather_error(runner: CliRunner, monkeypatch: pytest.MonkeyPatch) -> None:
    mock_run = AsyncMock(side_effect=ServiceError("All providers failed."))
    monkeypatch.setattr("weather.app.run", mock_run)
    result = runner.invoke(app)
    assert result.exit_code == 1
    assert "All providers failed." in result.stderr


def test_keyboard_interrupt(runner: CliRunner, monkeypatch: pytest.MonkeyPatch) -> None:
    mock_run = AsyncMock(side_effect=KeyboardInterrupt)
    monkeypatch.setattr("weather.app.run", mock_run)
    result = runner.invoke(app, ["-l", c.QUERY])
    assert result.exit_code == 130
    assert "Aborted" in result.stderr


def test_main_module_entrypoint(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_app = MagicMock()
    monkeypatch.setattr("weather.cli.app", mock_app)
    runpy.run_module("weather.__main__", run_name="__main__")
    mock_app.assert_called_once()


def test_main_module_import(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_app = MagicMock()
    monkeypatch.setattr("weather.cli.app", mock_app)
    import weather.__main__

    importlib.reload(weather.__main__)
    mock_app.assert_not_called()
