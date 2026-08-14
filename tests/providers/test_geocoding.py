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


async def test_nominatim_geocoding():
    payload = [
        NominatimResponse(
            lat=str(c.LATITUDE), lon=str(c.LONGITUDE), display_name=c.DISPLAY_NAME
        )
    ]
    transport = httpx.MockTransport(
        lambda req: httpx.Response(200, content=c.ENCODER.encode(payload))
    )

    async with httpx.AsyncClient(transport=transport) as client:
        provider = Nominatim(client)
        location = await provider.geocode(c.QUERY)

        assert location.latitude == c.LATITUDE
        assert location.longitude == c.LONGITUDE
        assert location.display_name == c.DISPLAY_NAME


async def test_nominatim_geocoding_not_found():
    transport = httpx.MockTransport(
        lambda req: httpx.Response(200, content=c.ENCODER.encode([]))
    )

    async with httpx.AsyncClient(transport=transport) as client:
        provider = Nominatim(client)
        with pytest.raises(LocationNotFoundError, match="No location found"):
            await provider.geocode(c.QUERY)


async def test_openmeteo_geocoding():
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
    transport = httpx.MockTransport(
        lambda req: httpx.Response(200, content=c.ENCODER.encode(payload))
    )

    async with httpx.AsyncClient(transport=transport) as client:
        provider = OpenMeteo(client)
        location = await provider.geocode(c.QUERY)

        assert location.latitude == c.LATITUDE
        assert location.longitude == c.LONGITUDE
        assert location.display_name == c.DISPLAY_NAME


async def test_openmeteo_geocoding_not_found():
    transport = httpx.MockTransport(
        lambda req: httpx.Response(200, content=c.ENCODER.encode(OpenMeteoResponse([])))
    )

    async with httpx.AsyncClient(transport=transport) as client:
        provider = OpenMeteo(client)
        with pytest.raises(LocationNotFoundError, match="No location found"):
            await provider.geocode(c.QUERY)
