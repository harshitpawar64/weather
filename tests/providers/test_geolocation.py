import httpx

import tests.constants as c
from weather.providers.geolocation import FreeIPAPI, IPInfo, IPWhoIs
from weather.providers.geolocation.freeipapi import FreeIPAPIResponse
from weather.providers.geolocation.ipinfo import IPInfoResponse
from weather.providers.geolocation.ipwhois import IPWhoIsResponse


async def test_freeipapi_geolocation():
    payload = FreeIPAPIResponse(
        latitude=c.LATITUDE,
        longitude=c.LONGITUDE,
        cityName=c.CITY,
        regionName=c.REGION,
        countryName=c.COUNTRY,
    )
    transport = httpx.MockTransport(
        lambda req: httpx.Response(200, content=c.ENCODER.encode(payload))
    )

    async with httpx.AsyncClient(transport=transport) as client:
        provider = FreeIPAPI(client)
        location = await provider.geolocate()

        assert location.latitude == c.LATITUDE
        assert location.longitude == c.LONGITUDE
        assert location.display_name == c.DISPLAY_NAME


async def test_ipinfo_geolocation():
    payload = IPInfoResponse(
        loc=f"{c.LATITUDE},{c.LONGITUDE}",
        city=c.CITY,
        region=c.REGION,
        country=c.COUNTRY,
    )
    transport = httpx.MockTransport(
        lambda req: httpx.Response(200, content=c.ENCODER.encode(payload))
    )

    async with httpx.AsyncClient(transport=transport) as client:
        provider = IPInfo(client)
        location = await provider.geolocate()

        assert location.latitude == c.LATITUDE
        assert location.longitude == c.LONGITUDE
        assert location.display_name == c.DISPLAY_NAME


async def test_ipwhois_geolocation():
    payload = IPWhoIsResponse(
        latitude=c.LATITUDE,
        longitude=c.LONGITUDE,
        city=c.CITY,
        region=c.REGION,
        country=c.COUNTRY,
    )
    transport = httpx.MockTransport(
        lambda req: httpx.Response(200, content=c.ENCODER.encode(payload))
    )

    async with httpx.AsyncClient(transport=transport) as client:
        provider = IPWhoIs(client)
        location = await provider.geolocate()

        assert location.latitude == c.LATITUDE
        assert location.longitude == c.LONGITUDE
        assert location.display_name == c.DISPLAY_NAME
