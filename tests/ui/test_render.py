from unittest.mock import MagicMock

import pytest

import tests.constants as c
from weather.models import Theme, UnitSystem, WeatherData, WeatherResponse
from weather.ui.render import render_weather


def test_single_day(monkeypatch: pytest.MonkeyPatch) -> None:
    response = WeatherResponse(
        location=c.LOCATION, weather=c.WEATHER_DATA, aqi=c.AIR_QUALITY
    )
    mock_print = MagicMock()
    monkeypatch.setattr("weather.ui.render.console.print", mock_print)

    render_weather(response, theme=Theme.DEFAULT, days=1)
    assert mock_print.call_count == 1


def test_multi_day(monkeypatch: pytest.MonkeyPatch) -> None:
    daily = [c.DAILY_FORECAST, c.DAILY_FORECAST]
    weather_obj = WeatherData(
        current=c.CURRENT_WEATHER,
        daily=daily,
        unit_system=UnitSystem.METRIC,
        valid_until=c.AIR_QUALITY.valid_until,
    )
    response = WeatherResponse(
        location=c.LOCATION, weather=weather_obj, aqi=c.AIR_QUALITY
    )
    mock_print = MagicMock()
    monkeypatch.setattr("weather.ui.render.console.print", mock_print)

    render_weather(response, theme=Theme.DEFAULT, days=2)
    assert mock_print.call_count == 3
