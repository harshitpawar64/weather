from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

import tests.constants as c
from weather.exceptions import ProviderError, ServiceError
from weather.services.geolocation import GeolocationService


async def test_geolocation_service_primary_provider_success(
    mock_client: MagicMock,
) -> None:
    mock_primary = AsyncMock()
    mock_primary.is_configured = True
    mock_primary.geolocate.return_value = c.LOCATION

    mock_secondary = AsyncMock()

    service = GeolocationService(mock_client)
    service.providers = (mock_primary, mock_secondary)

    result = await service.geolocate()

    assert result == c.LOCATION
    mock_primary.geolocate.assert_awaited_once()
    mock_secondary.geolocate.assert_not_called()


async def test_geolocation_service_fallback_chain(mock_client: MagicMock) -> None:
    mock_1 = AsyncMock()
    mock_1.is_configured = True
    mock_1.geolocate.side_effect = httpx.ConnectError("Connection failed")

    mock_2 = AsyncMock()
    mock_2.is_configured = False  # Unconfigured provider skipped

    mock_3 = AsyncMock()
    mock_3.is_configured = True
    mock_3.geolocate.side_effect = ProviderError("Rate limited")

    mock_4 = AsyncMock()
    mock_4.is_configured = True
    mock_4.geolocate.return_value = c.LOCATION

    service = GeolocationService(mock_client)
    service.providers = (mock_1, mock_2, mock_3, mock_4)

    result = await service.geolocate()

    assert result == c.LOCATION
    mock_1.geolocate.assert_awaited_once()
    mock_2.geolocate.assert_not_called()
    mock_3.geolocate.assert_awaited_once()
    mock_4.geolocate.assert_awaited_once()


async def test_geolocation_service_all_providers_fail(mock_client: MagicMock) -> None:
    mock_1 = AsyncMock()
    mock_1.is_configured = True
    mock_1.geolocate.side_effect = httpx.HTTPError("HTTP error")

    mock_2 = AsyncMock()
    mock_2.is_configured = True
    mock_2.geolocate.side_effect = ProviderError("Provider error")

    service = GeolocationService(mock_client)
    service.providers = (mock_1, mock_2)

    with pytest.raises(ServiceError, match="All geolocation providers failed."):
        await service.geolocate()
