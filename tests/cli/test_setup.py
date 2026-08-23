from unittest.mock import AsyncMock

import pytest
from typer.testing import CliRunner

from weather.cli import app


def test_setup(runner: CliRunner, monkeypatch: pytest.MonkeyPatch) -> None:
    mock_setup = AsyncMock()
    monkeypatch.setattr("weather.app.run_setup", mock_setup)
    result = runner.invoke(app, ["setup"])
    assert result.exit_code == 0
    mock_setup.assert_awaited_once()


def test_keyboard_interrupt(runner: CliRunner, monkeypatch: pytest.MonkeyPatch) -> None:
    mock_setup = AsyncMock(side_effect=KeyboardInterrupt)
    monkeypatch.setattr("weather.app.run_setup", mock_setup)
    result = runner.invoke(app, ["setup"])
    assert result.exit_code == 130
    assert "Aborted" in result.stderr
