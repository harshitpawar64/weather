from unittest.mock import AsyncMock, MagicMock

import pytest

import tests.constants as c
from weather.exceptions import ServiceError
from weather.models import UnitSystem
from weather.onboarding import onboarding


async def test_auto_location_accepted(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_geolocator = AsyncMock()
    mock_geolocator.geolocate.return_value = c.LOCATION

    mock_geocoder = AsyncMock()

    monkeypatch.setattr("weather.onboarding.Confirm.ask", lambda *a, **k: True)
    monkeypatch.setattr("weather.onboarding.Prompt.ask", lambda *a, **k: "metric")

    location, unit_system = await onboarding(mock_geolocator, mock_geocoder)

    assert location == c.LOCATION
    assert unit_system == UnitSystem.METRIC
    mock_geolocator.geolocate.assert_awaited_once()
    mock_geocoder.geocode.assert_not_called()


async def test_auto_location_declined_manual_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_geolocator = AsyncMock()
    mock_geolocator.geolocate.return_value = c.LOCATION

    mock_geocoder = AsyncMock()
    mock_geocoder.geocode.return_value = c.LOCATION

    monkeypatch.setattr("weather.onboarding.Confirm.ask", lambda *a, **k: False)
    monkeypatch.setattr(
        "weather.onboarding.Prompt.ask", MagicMock(side_effect=[c.QUERY, "imperial"])
    )

    location, unit_system = await onboarding(mock_geolocator, mock_geocoder)

    assert location == c.LOCATION
    assert unit_system == UnitSystem.IMPERIAL
    mock_geocoder.geocode.assert_awaited_once_with(c.QUERY)


async def test_geolocator_error_manual_retry(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_geolocator = AsyncMock()
    mock_geolocator.geolocate.side_effect = ServiceError(
        "All geolocation providers failed."
    )

    mock_geocoder = AsyncMock()
    mock_geocoder.geocode.side_effect = [ServiceError("Search failed"), c.LOCATION]

    monkeypatch.setattr(
        "weather.onboarding.Prompt.ask",
        MagicMock(side_effect=["", "bad_query", c.QUERY, "metric"]),
    )

    location, unit_system = await onboarding(mock_geolocator, mock_geocoder)

    assert location == c.LOCATION
    assert unit_system == UnitSystem.METRIC
    assert mock_geocoder.geocode.await_count == 2
