from unittest.mock import AsyncMock, MagicMock

import pytest
from typer.testing import CliRunner

import tests.constants as c
from weather.cli import app
from weather.config import Config
from weather.exceptions import ServiceError
from weather.models import Theme, UnitSystem
from weather.services import GeocodingService


def test_path(runner: CliRunner) -> None:
    result = runner.invoke(app, ["config", "path"])
    assert result.exit_code == 0
    assert "config.toml" in result.stdout


def test_show_default(runner: CliRunner, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(Config, "location", None)
    monkeypatch.setattr(Config, "unit_system", UnitSystem.METRIC)
    monkeypatch.setattr(Config, "theme", Theme.DEFAULT)
    result = runner.invoke(app, ["config", "show"])
    assert result.exit_code == 0
    assert "Location:" in result.stdout
    assert "Not set" in result.stdout
    assert "Units:" in result.stdout
    assert "metric" in result.stdout
    assert "Theme:" in result.stdout
    assert "default" in result.stdout


def test_show_configured(runner: CliRunner, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(Config, "location", c.LOCATION)
    monkeypatch.setattr(Config, "unit_system", UnitSystem.IMPERIAL)
    monkeypatch.setattr(Config, "theme", Theme.DEFAULT)
    result = runner.invoke(app, ["config", "show"])
    assert result.exit_code == 0
    assert c.LOCATION.display_name in result.stdout
    assert "imperial" in result.stdout
    assert "default" in result.stdout


def test_set_no_options(runner: CliRunner) -> None:
    result = runner.invoke(app, ["config", "set"])
    assert result.exit_code == 0
    assert "No configuration options specified" in result.stdout


def test_set_units_and_theme(
    runner: CliRunner, monkeypatch: pytest.MonkeyPatch
) -> None:
    mock_save = MagicMock()
    monkeypatch.setattr(Config, "save", mock_save)
    result = runner.invoke(
        app, ["config", "set", "--units", "imperial", "--theme", "default"]
    )
    assert result.exit_code == 0
    assert "Configuration updated successfully" in result.stdout
    mock_save.assert_called_once_with(
        location=None, unit_system=UnitSystem.IMPERIAL, theme=Theme.DEFAULT
    )


def test_set_location_success(
    runner: CliRunner, monkeypatch: pytest.MonkeyPatch
) -> None:
    mock_save = MagicMock()
    monkeypatch.setattr(Config, "save", mock_save)
    monkeypatch.setattr(GeocodingService, "geocode", AsyncMock(return_value=c.LOCATION))
    result = runner.invoke(app, ["config", "set", "-l", "Paris"])
    assert result.exit_code == 0
    assert "Configuration updated successfully" in result.stdout
    mock_save.assert_called_once_with(location=c.LOCATION, unit_system=None, theme=None)


def test_set_location_failure(
    runner: CliRunner, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        GeocodingService,
        "geocode",
        AsyncMock(side_effect=ServiceError("All geocoding providers failed.")),
    )
    result = runner.invoke(app, ["config", "set", "-l", "InvalidPlace"])
    assert result.exit_code == 1
    assert "Could not find location 'InvalidPlace'" in result.stderr


def test_set_location_keyboard_interrupt(
    runner: CliRunner, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        GeocodingService, "geocode", AsyncMock(side_effect=KeyboardInterrupt)
    )
    result = runner.invoke(app, ["config", "set", "-l", "Paris"])
    assert result.exit_code == 130
    assert "Aborted." in result.stderr


def test_reset_success(runner: CliRunner, monkeypatch: pytest.MonkeyPatch) -> None:
    mock_reset = MagicMock()
    monkeypatch.setattr(Config, "reset", mock_reset)
    result = runner.invoke(app, ["config", "reset"])
    assert result.exit_code == 0
    assert "Configuration reset to defaults" in result.stdout
    mock_reset.assert_called_once()


def test_reset_error(runner: CliRunner, monkeypatch: pytest.MonkeyPatch) -> None:
    mock_reset = MagicMock(side_effect=PermissionError("Permission denied"))
    monkeypatch.setattr(Config, "reset", mock_reset)
    result = runner.invoke(app, ["config", "reset"])
    assert result.exit_code == 1
    assert "Failed to reset config: Permission denied" in result.stderr
