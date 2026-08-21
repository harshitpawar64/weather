from unittest.mock import AsyncMock, MagicMock

import pytest

import tests.constants as c
import weather.app
from weather.exceptions import ServiceError
from weather.models import Theme, UnitSystem
from weather.services import AQIService, GeocodingService, WeatherService


async def test_app_run_with_query_json_output(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    mock_geocode = AsyncMock(return_value=c.LOCATION)
    mock_weather = AsyncMock(return_value=c.WEATHER_DATA)
    mock_aqi = AsyncMock(return_value=c.AIR_QUALITY)

    monkeypatch.setattr(GeocodingService, "geocode", mock_geocode)
    monkeypatch.setattr(WeatherService, "get_weather", mock_weather)
    monkeypatch.setattr(AQIService, "get_aqi", mock_aqi)

    await weather.app.run(
        query=c.QUERY,
        unit_system=UnitSystem.METRIC,
        theme=Theme.DEFAULT,
        days=1,
        json_output=True,
    )

    captured = capsys.readouterr()
    assert c.CITY in captured.out
    assert '"us_aqi":42.0' in captured.out


async def test_app_run_with_saved_config_renders(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_weather = AsyncMock(return_value=c.WEATHER_DATA)
    mock_aqi = AsyncMock(return_value=c.AIR_QUALITY)
    mock_render = MagicMock()

    monkeypatch.setattr(weather.app.Config, "location", c.LOCATION)
    monkeypatch.setattr(WeatherService, "get_weather", mock_weather)
    monkeypatch.setattr(AQIService, "get_aqi", mock_aqi)
    monkeypatch.setattr("weather.app.render_weather", mock_render)

    await weather.app.run(
        query=None,
        unit_system=UnitSystem.METRIC,
        theme=Theme.DEFAULT,
        days=7,
        json_output=False,
    )

    mock_render.assert_called_once()


async def test_app_run_triggers_onboarding_when_no_config(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_onboarding = AsyncMock(return_value=(c.LOCATION, UnitSystem.METRIC))
    mock_weather = AsyncMock(return_value=c.WEATHER_DATA)
    mock_aqi = AsyncMock(return_value=c.AIR_QUALITY)
    mock_save = MagicMock()

    monkeypatch.setattr(weather.app.Config, "location", None)
    monkeypatch.setattr(weather.app.config, "save", mock_save)
    monkeypatch.setattr("weather.app.onboarding", mock_onboarding)
    monkeypatch.setattr(WeatherService, "get_weather", mock_weather)
    monkeypatch.setattr(AQIService, "get_aqi", mock_aqi)
    monkeypatch.setattr("weather.app.render_weather", MagicMock())

    await weather.app.run(
        query=None,
        unit_system=UnitSystem.METRIC,
        theme=Theme.DEFAULT,
        days=1,
        json_output=False,
    )

    mock_onboarding.assert_awaited_once()
    mock_save.assert_called_once_with(c.LOCATION, UnitSystem.METRIC)


async def test_app_run_aqi_exception_handled_as_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_weather = AsyncMock(return_value=c.WEATHER_DATA)
    mock_aqi = AsyncMock(side_effect=ServiceError("AQI provider failed"))
    mock_render = MagicMock()

    monkeypatch.setattr(weather.app.Config, "location", c.LOCATION)
    monkeypatch.setattr(WeatherService, "get_weather", mock_weather)
    monkeypatch.setattr(AQIService, "get_aqi", mock_aqi)
    monkeypatch.setattr("weather.app.render_weather", mock_render)

    await weather.app.run(
        query=None,
        unit_system=UnitSystem.METRIC,
        theme=Theme.DEFAULT,
        days=1,
        json_output=False,
    )

    response = mock_render.call_args[0][0]
    assert response.aqi is None


async def test_app_run_weather_exception_propagates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_weather = AsyncMock(side_effect=ServiceError("All weather providers failed."))
    mock_aqi = AsyncMock(return_value=c.AIR_QUALITY)

    monkeypatch.setattr(weather.app.Config, "location", c.LOCATION)
    monkeypatch.setattr(WeatherService, "get_weather", mock_weather)
    monkeypatch.setattr(AQIService, "get_aqi", mock_aqi)

    with pytest.raises(ServiceError, match="All weather providers failed."):
        await weather.app.run(
            query=None,
            unit_system=UnitSystem.METRIC,
            theme=Theme.DEFAULT,
            days=1,
            json_output=False,
        )


async def test_app_run_setup(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_onboarding = AsyncMock(return_value=(c.LOCATION, UnitSystem.METRIC))
    mock_save = MagicMock()

    monkeypatch.setattr("weather.app.onboarding", mock_onboarding)
    monkeypatch.setattr(weather.app.config, "save", mock_save)

    await weather.app.run_setup()

    mock_onboarding.assert_awaited_once()
    mock_save.assert_called_once_with(c.LOCATION, UnitSystem.METRIC)
