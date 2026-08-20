import time
from collections.abc import Callable
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

import tests.constants as c
from weather.cache import Cache
from weather.exceptions import ServiceError
from weather.models import UnitSystem, WeatherData
from weather.services.weather import WeatherService


async def test_weather_service_cache_hit(
    cache: Cache,
    make_weather: Callable[..., WeatherData],
    mock_client: MagicMock,
) -> None:
    cached_weather = make_weather(valid_until=time.time() + 3600)
    cache.save(location=c.LOCATION, weather=cached_weather)

    mock_provider = AsyncMock()
    service = WeatherService(mock_client, cache)
    service.providers = (mock_provider,)

    result = await service.get_weather(c.LOCATION, UnitSystem.METRIC)

    assert result == cached_weather
    mock_provider.fetch_weather.assert_not_called()


async def test_weather_service_provider_success(
    cache: Cache,
    make_weather: Callable[..., WeatherData],
    mock_client: MagicMock,
) -> None:
    expected_weather = make_weather(valid_until=time.time() + 3600)

    mock_provider = AsyncMock()
    mock_provider.is_configured = True
    mock_provider.fetch_weather.return_value = expected_weather

    service = WeatherService(mock_client, cache)
    service.providers = (mock_provider,)

    result = await service.get_weather(c.LOCATION, UnitSystem.METRIC)

    assert result == expected_weather
    mock_provider.fetch_weather.assert_awaited_once_with(c.LOCATION, UnitSystem.METRIC)


async def test_weather_service_fallback_to_stale_cache(
    cache: Cache,
    make_weather: Callable[..., WeatherData],
    mock_client: MagicMock,
) -> None:
    stale_weather = make_weather(valid_until=time.time() - 3600)
    cache.save(location=c.LOCATION, weather=stale_weather)

    failing_provider = AsyncMock()
    failing_provider.is_configured = True
    failing_provider.fetch_weather.side_effect = httpx.ConnectError("Network error")

    service = WeatherService(mock_client, cache)
    service.providers = (failing_provider,)

    result = await service.get_weather(c.LOCATION, UnitSystem.METRIC)

    assert result == stale_weather


async def test_weather_service_all_providers_fail_no_cache(
    cache: Cache,
    mock_client: MagicMock,
) -> None:
    failing_provider = AsyncMock()
    failing_provider.is_configured = True
    failing_provider.fetch_weather.side_effect = httpx.HTTPStatusError(
        "500 Internal Server Error",
        request=httpx.Request("GET", "https://api.open-meteo.com"),
        response=httpx.Response(500),
    )

    service = WeatherService(mock_client, cache)
    service.providers = (failing_provider,)

    with pytest.raises(ServiceError, match="All weather providers failed."):
        await service.get_weather(c.LOCATION, UnitSystem.METRIC)


async def test_weather_service_skips_unconfigured_provider(
    cache: Cache,
    mock_client: MagicMock,
) -> None:
    unconfigured_provider = AsyncMock()
    unconfigured_provider.is_configured = False

    service = WeatherService(mock_client, cache)
    service.providers = (unconfigured_provider,)

    with pytest.raises(ServiceError, match="All weather providers failed."):
        await service.get_weather(c.LOCATION, UnitSystem.METRIC)

    unconfigured_provider.fetch_weather.assert_not_called()
