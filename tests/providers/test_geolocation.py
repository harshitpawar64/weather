from collections.abc import Callable

import httpx
import pytest

import tests.constants as c
from weather.exceptions import ProviderError
from weather.providers.geolocation import CountryIs, FreeIPAPI, IPInfo, IPWhoIs
from weather.providers.geolocation.countryis import CountryIsLocation, CountryIsResponse
from weather.providers.geolocation.freeipapi import FreeIPAPIResponse
from weather.providers.geolocation.ipinfo import IPInfoResponse
from weather.providers.geolocation.ipwhois import IPWhoIsResponse


async def test_countryis_geolocation(
    mock_http_client: Callable[..., httpx.AsyncClient],
) -> None:
    payload = CountryIsResponse(
        location=CountryIsLocation(latitude=c.LATITUDE, longitude=c.LONGITUDE),
        city=c.CITY,
        country=c.COUNTRY,
    )

    async with mock_http_client(payload) as client:
        provider = CountryIs(client)
        location = await provider.geolocate()

        assert location.latitude == c.LATITUDE
        assert location.longitude == c.LONGITUDE
        assert location.display_name == f"{c.CITY}, {c.COUNTRY}"


async def test_freeipapi_geolocation(
    mock_http_client: Callable[..., httpx.AsyncClient],
) -> None:
    payload = FreeIPAPIResponse(
        latitude=c.LATITUDE,
        longitude=c.LONGITUDE,
        cityName=c.CITY,
        regionName=c.REGION,
        countryName=c.COUNTRY,
    )

    async with mock_http_client(payload) as client:
        provider = FreeIPAPI(client)
        location = await provider.geolocate()

        assert location.latitude == c.LATITUDE
        assert location.longitude == c.LONGITUDE
        assert location.display_name == c.DISPLAY_NAME


async def test_ipinfo_geolocation(
    mock_http_client: Callable[..., httpx.AsyncClient],
) -> None:
    payload = IPInfoResponse(
        loc=f"{c.LATITUDE},{c.LONGITUDE}",
        city=c.CITY,
        region=c.REGION,
        country=c.COUNTRY,
    )

    async with mock_http_client(payload) as client:
        provider = IPInfo(client)
        location = await provider.geolocate()

        assert location.latitude == c.LATITUDE
        assert location.longitude == c.LONGITUDE
        assert location.display_name == c.DISPLAY_NAME


async def test_ipinfo_invalid_coordinates(
    mock_http_client: Callable[..., httpx.AsyncClient],
) -> None:
    payload = IPInfoResponse(
        loc="invalid_loc", city=c.CITY, region=c.REGION, country=c.COUNTRY
    )

    async with mock_http_client(payload) as client:
        provider = IPInfo(client)
        with pytest.raises(ProviderError, match="Invalid coordinates: 'invalid_loc'"):
            await provider.geolocate()


async def test_ipwhois_geolocation(
    mock_http_client: Callable[..., httpx.AsyncClient],
) -> None:
    payload = IPWhoIsResponse(
        latitude=c.LATITUDE,
        longitude=c.LONGITUDE,
        city=c.CITY,
        region=c.REGION,
        country=c.COUNTRY,
    )

    async with mock_http_client(payload) as client:
        provider = IPWhoIs(client)
        location = await provider.geolocate()

        assert location.latitude == c.LATITUDE
        assert location.longitude == c.LONGITUDE
        assert location.display_name == c.DISPLAY_NAME
