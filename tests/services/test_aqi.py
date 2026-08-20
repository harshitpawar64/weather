import time
from collections.abc import Callable
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

import tests.constants as c
from weather.cache import Cache
from weather.exceptions import ProviderError, ServiceError
from weather.models import AirQuality, WeatherData
from weather.services.aqi import AQIService


async def test_aqi_service_cache_hit(
    cache: Cache,
    make_aqi: Callable[..., AirQuality],
    make_weather: Callable[..., WeatherData],
    mock_client: MagicMock,
) -> None:
    cached_aqi = make_aqi(valid_until=time.time() + 3600)
    weather_dummy = make_weather(valid_until=time.time() + 3600)
    cache.save(location=c.LOCATION, weather=weather_dummy, aqi=cached_aqi)

    mock_provider = AsyncMock()
    service = AQIService(mock_client, cache)
    service.providers = (mock_provider,)

    result = await service.get_aqi(c.LOCATION)

    assert result == cached_aqi
    mock_provider.fetch_aqi.assert_not_called()


async def test_aqi_service_primary_provider_success(
    cache: Cache,
    make_aqi: Callable[..., AirQuality],
    mock_client: MagicMock,
) -> None:
    expected_aqi = make_aqi(valid_until=time.time() + 3600)

    mock_primary = AsyncMock()
    mock_primary.is_configured = True
    mock_primary.fetch_aqi.return_value = expected_aqi

    mock_secondary = AsyncMock()

    service = AQIService(mock_client, cache)
    service.providers = (mock_primary, mock_secondary)

    result = await service.get_aqi(c.LOCATION)

    assert result == expected_aqi
    mock_primary.fetch_aqi.assert_awaited_once_with(c.LOCATION)
    mock_secondary.fetch_aqi.assert_not_called()


async def test_aqi_service_fallback_to_secondary_provider(
    cache: Cache,
    make_aqi: Callable[..., AirQuality],
    mock_client: MagicMock,
) -> None:
    expected_aqi = make_aqi(valid_until=time.time() + 3600)

    mock_primary = AsyncMock()
    mock_primary.is_configured = True
    mock_primary.fetch_aqi.side_effect = httpx.ConnectError("OpenMeteo unreachable")

    mock_secondary = AsyncMock()
    mock_secondary.is_configured = True
    mock_secondary.fetch_aqi.return_value = expected_aqi

    service = AQIService(mock_client, cache)
    service.providers = (mock_primary, mock_secondary)

    result = await service.get_aqi(c.LOCATION)

    assert result == expected_aqi
    mock_primary.fetch_aqi.assert_awaited_once_with(c.LOCATION)
    mock_secondary.fetch_aqi.assert_awaited_once_with(c.LOCATION)


async def test_aqi_service_skips_unconfigured_provider(
    cache: Cache,
    make_aqi: Callable[..., AirQuality],
    mock_client: MagicMock,
) -> None:
    expected_aqi = make_aqi(valid_until=time.time() + 3600)

    mock_primary = AsyncMock()
    mock_primary.is_configured = False

    mock_secondary = AsyncMock()
    mock_secondary.is_configured = True
    mock_secondary.fetch_aqi.return_value = expected_aqi

    service = AQIService(mock_client, cache)
    service.providers = (mock_primary, mock_secondary)

    result = await service.get_aqi(c.LOCATION)

    assert result == expected_aqi
    mock_primary.fetch_aqi.assert_not_called()
    mock_secondary.fetch_aqi.assert_awaited_once_with(c.LOCATION)


async def test_aqi_service_fallback_to_stale_cache(
    cache: Cache,
    make_aqi: Callable[..., AirQuality],
    make_weather: Callable[..., WeatherData],
    mock_client: MagicMock,
) -> None:
    stale_aqi = make_aqi(valid_until=time.time() - 3600)
    weather_dummy = make_weather(valid_until=time.time() + 3600)
    cache.save(location=c.LOCATION, weather=weather_dummy, aqi=stale_aqi)

    failing_provider = AsyncMock()
    failing_provider.is_configured = True
    failing_provider.fetch_aqi.side_effect = ProviderError("API failure")

    service = AQIService(mock_client, cache)
    service.providers = (failing_provider,)

    result = await service.get_aqi(c.LOCATION)

    assert result == stale_aqi


async def test_aqi_service_all_providers_fail_no_cache(
    cache: Cache,
    mock_client: MagicMock,
) -> None:
    failing_provider = AsyncMock()
    failing_provider.is_configured = True
    failing_provider.fetch_aqi.side_effect = ProviderError("API failure")

    service = AQIService(mock_client, cache)
    service.providers = (failing_provider,)

    with pytest.raises(ServiceError, match="All AQI providers failed."):
        await service.get_aqi(c.LOCATION)
