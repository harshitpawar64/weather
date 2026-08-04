import httpx

import tests.constants as c
from weather.models import UnixTimestamp
from weather.providers.aqi import OpenMeteo, OpenWeather
from weather.providers.aqi.openmeteo import OpenMeteoCurrentResponse, OpenMeteoResponse
from weather.providers.aqi.openweather import (
    OpenWeatherComponents,
    OpenWeatherList,
    OpenWeatherResponse,
)
from weather.utils import get_us_aqi


async def test_openmeteo_aqi_fetch():
    current_payload = OpenMeteoCurrentResponse(
        time="1970-01-01T00:00", interval=3600, us_aqi=42, pm10=18.5, pm2_5=9.2
    )
    payload = OpenMeteoResponse(utc_offset_seconds=0, current=current_payload)

    transport = httpx.MockTransport(
        lambda req: httpx.Response(200, content=c.ENCODER.encode(payload))
    )

    async with httpx.AsyncClient(transport=transport) as client:
        provider = OpenMeteo(client)
        aqi_data = await provider.fetch_aqi(c.LOCATION)

        assert aqi_data.us_aqi == 42.0
        assert aqi_data.pm_2_5 == 9.2
        assert aqi_data.pm_10 == 18.5


async def test_openweather_aqi_fetch():
    components = OpenWeatherComponents(pm2_5=5.0, pm10=25.0)
    item = OpenWeatherList(dt=UnixTimestamp(0.0), components=components)
    payload = OpenWeatherResponse(items=[item])

    transport = httpx.MockTransport(
        lambda req: httpx.Response(200, content=c.ENCODER.encode(payload))
    )

    async with httpx.AsyncClient(transport=transport) as client:
        provider = OpenWeather(client)
        aqi_data = await provider.fetch_aqi(c.LOCATION)

        assert aqi_data.pm_2_5 == 5.0
        assert aqi_data.pm_10 == 25.0
        assert aqi_data.us_aqi == get_us_aqi(5.0, 25.0)
        assert aqi_data.valid_until == 3600.0
