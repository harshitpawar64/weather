from collections.abc import Callable
from unittest.mock import MagicMock

import httpx
import pytest

import tests.constants as c
from weather.exceptions import ProviderError
from weather.models import UnixTimestamp
from weather.providers.aqi import OpenMeteo, OpenWeather
from weather.providers.aqi.openmeteo import OpenMeteoCurrentResponse, OpenMeteoResponse
from weather.providers.aqi.openweather import (
    OpenWeatherComponents,
    OpenWeatherList,
    OpenWeatherResponse,
)
from weather.utils import get_us_aqi


async def test_openmeteo_aqi_fetch(
    mock_http_client: Callable[..., httpx.AsyncClient],
) -> None:
    current_payload = OpenMeteoCurrentResponse(
        time=c.TIME, interval=3600, us_aqi=42, pm10=18.5, pm2_5=9.2
    )
    payload = OpenMeteoResponse(utc_offset_seconds=0, current=current_payload)

    async with mock_http_client(payload) as client:
        provider = OpenMeteo(client)
        aqi_data = await provider.fetch_aqi(c.LOCATION)

        assert aqi_data.us_aqi == 42.0
        assert aqi_data.pm_2_5 == 9.2
        assert aqi_data.pm_10 == 18.5


async def test_openweather_aqi_fetch(
    monkeypatch: pytest.MonkeyPatch, mock_http_client: Callable[..., httpx.AsyncClient]
) -> None:
    monkeypatch.setenv("OPENWEATHER_API_KEY", "test_key")
    components = OpenWeatherComponents(pm2_5=5.0, pm10=25.0)
    item = OpenWeatherList(dt=UnixTimestamp(0.0), components=components)
    payload = OpenWeatherResponse(items=[item])

    async with mock_http_client(payload) as client:
        provider = OpenWeather(client)
        assert provider.is_configured is True
        aqi_data = await provider.fetch_aqi(c.LOCATION)

        assert aqi_data.pm_2_5 == 5.0
        assert aqi_data.pm_10 == 25.0
        assert aqi_data.us_aqi == get_us_aqi(5.0, 25.0)
        assert aqi_data.valid_until == 3600.0


async def test_openweather_unconfigured(
    monkeypatch: pytest.MonkeyPatch, mock_client: MagicMock
) -> None:
    monkeypatch.delenv("OPENWEATHER_API_KEY", raising=False)

    provider = OpenWeather(mock_client)
    assert provider.is_configured is False
    with pytest.raises(
        ProviderError,
        match="OPENWEATHER_API_KEY environment variable is not set or is empty.",
    ):
        await provider.fetch_aqi(c.LOCATION)
