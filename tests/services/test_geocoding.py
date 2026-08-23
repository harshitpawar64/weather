from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

import tests.constants as c
from weather.cache import Cache
from weather.exceptions import LocationNotFoundError, ServiceError
from weather.services.geocoding import GeocodingService


async def test_cache_hit(cache: Cache, mock_client: MagicMock) -> None:
    cache.save(location=c.LOCATION, weather=c.WEATHER_DATA, query=c.QUERY)

    mock_provider = AsyncMock()
    service = GeocodingService(mock_client, cache)
    service.providers = (mock_provider,)

    result = await service.geocode(c.QUERY)

    assert result == c.LOCATION
    assert result.display_name == c.DISPLAY_NAME
    mock_provider.geocode.assert_not_called()


async def test_primary_provider_success(cache: Cache, mock_client: MagicMock) -> None:
    mock_primary = AsyncMock()
    mock_primary.is_configured = True
    mock_primary.geocode.return_value = c.LOCATION

    mock_secondary = AsyncMock()

    service = GeocodingService(mock_client, cache)
    service.providers = (mock_primary, mock_secondary)

    result = await service.geocode(c.QUERY)

    assert result == c.LOCATION
    mock_primary.geocode.assert_awaited_once_with(c.QUERY)
    mock_secondary.geocode.assert_not_called()


async def test_fallback_to_secondary_provider(
    cache: Cache, mock_client: MagicMock
) -> None:
    mock_primary = AsyncMock()
    mock_primary.is_configured = True
    mock_primary.geocode.side_effect = LocationNotFoundError("Nominatim not found")

    mock_secondary = AsyncMock()
    mock_secondary.is_configured = True
    mock_secondary.geocode.return_value = c.LOCATION

    service = GeocodingService(mock_client, cache)
    service.providers = (mock_primary, mock_secondary)

    result = await service.geocode(c.QUERY)

    assert result == c.LOCATION
    mock_primary.geocode.assert_awaited_once_with(c.QUERY)
    mock_secondary.geocode.assert_awaited_once_with(c.QUERY)


async def test_skips_unconfigured_provider(
    cache: Cache, mock_client: MagicMock
) -> None:
    mock_primary = AsyncMock()
    mock_primary.is_configured = False

    mock_secondary = AsyncMock()
    mock_secondary.is_configured = True
    mock_secondary.geocode.return_value = c.LOCATION

    service = GeocodingService(mock_client, cache)
    service.providers = (mock_primary, mock_secondary)

    result = await service.geocode(c.QUERY)

    assert result == c.LOCATION
    mock_primary.geocode.assert_not_called()
    mock_secondary.geocode.assert_awaited_once_with(c.QUERY)


async def test_all_providers_fail(cache: Cache, mock_client: MagicMock) -> None:
    mock_primary = AsyncMock()
    mock_primary.is_configured = True
    mock_primary.geocode.side_effect = httpx.ConnectError("Network error")

    mock_secondary = AsyncMock()
    mock_secondary.is_configured = True
    mock_secondary.geocode.side_effect = LocationNotFoundError("Not found")

    service = GeocodingService(mock_client, cache)
    service.providers = (mock_primary, mock_secondary)

    with pytest.raises(ServiceError, match="All geocoding providers failed."):
        await service.geocode(c.QUERY)
