from collections.abc import Callable

import httpx
import pytest

import tests.constants as c
from weather.exceptions import LocationNotFoundError
from weather.providers.geocoding import Nominatim, OpenMeteo
from weather.providers.geocoding.nominatim import NominatimResponse
from weather.providers.geocoding.openmeteo import (
    OpenMeteoResponse,
    OpenMeteoResultResponse,
)


async def test_nominatim_geocoding(
    mock_http_client: Callable[..., httpx.AsyncClient],
) -> None:
    payload = [
        NominatimResponse(
            lat=str(c.LATITUDE), lon=str(c.LONGITUDE), display_name=c.DISPLAY_NAME
        )
    ]

    async with mock_http_client(payload) as client:
        provider = Nominatim(client)
        location = await provider.geocode(c.QUERY)

        assert location.latitude == c.LATITUDE
        assert location.longitude == c.LONGITUDE
        assert location.display_name == c.DISPLAY_NAME


async def test_nominatim_geocoding_not_found(
    mock_http_client: Callable[..., httpx.AsyncClient],
) -> None:
    async with mock_http_client([]) as client:
        provider = Nominatim(client)
        with pytest.raises(LocationNotFoundError, match="No location found"):
            await provider.geocode(c.QUERY)


async def test_openmeteo_geocoding(
    mock_http_client: Callable[..., httpx.AsyncClient],
) -> None:
    payload = OpenMeteoResponse(
        results=[
            OpenMeteoResultResponse(
                latitude=c.LATITUDE,
                longitude=c.LONGITUDE,
                name=c.CITY,
                admin1=c.REGION,
                country=c.COUNTRY,
            )
        ]
    )

    async with mock_http_client(payload) as client:
        provider = OpenMeteo(client)
        location = await provider.geocode(c.QUERY)

        assert location.latitude == c.LATITUDE
        assert location.longitude == c.LONGITUDE
        assert location.display_name == c.DISPLAY_NAME


async def test_openmeteo_geocoding_not_found(
    mock_http_client: Callable[..., httpx.AsyncClient],
) -> None:
    async with mock_http_client(OpenMeteoResponse([])) as client:
        provider = OpenMeteo(client)
        with pytest.raises(LocationNotFoundError, match="No location found"):
            await provider.geocode(c.QUERY)
