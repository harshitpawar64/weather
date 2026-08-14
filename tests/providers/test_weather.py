import httpx

import tests.constants as c
from weather.models import UnitSystem
from weather.providers.weather import OpenMeteo
from weather.providers.weather.openmeteo import (
    OpenMeteoCurrentResponse,
    OpenMeteoDailyResponse,
)
from weather.providers.weather.openmeteo import (
    OpenMeteoResponse as OpenMeteoWeatherResponse,
)


async def test_openmeteo_weather():
    current_payload = OpenMeteoCurrentResponse(
        time="1970-01-01T00:00",
        interval=900,
        weather_code=0,
        temperature_2m=20.0,
        apparent_temperature=19.5,
        relative_humidity_2m=50,
        precipitation=0.0,
        wind_speed_10m=10.0,
        wind_direction_10m=180,
        wind_gusts_10m=12.0,
        is_day=1,
    )
    daily_payload = OpenMeteoDailyResponse(
        time=["1970-01-01"],
        weather_code=[0],
        temperature_2m_min=[15.0],
        temperature_2m_max=[25.0],
        precipitation_sum=[0.0],
        precipitation_probability_max=[10],
        wind_speed_10m_max=[15.0],
        sunrise=["1970-01-01T05:00"],
        sunset=["1970-01-01T21:00"],
    )
    payload = OpenMeteoWeatherResponse(
        utc_offset_seconds=0, current=current_payload, daily=daily_payload
    )

    transport = httpx.MockTransport(
        lambda req: httpx.Response(200, content=c.ENCODER.encode(payload))
    )

    async with httpx.AsyncClient(transport=transport) as client:
        provider = OpenMeteo(client)
        weather_data = await provider.fetch_weather(c.LOCATION, UnitSystem.METRIC)

        assert weather_data.current.temperature == 20.0
        assert weather_data.current.is_day is True
        assert weather_data.unit_system == UnitSystem.METRIC
        assert len(weather_data.daily) == 1
        assert weather_data.daily[0].temp_max == 25.0

        weather_data_imperial = await provider.fetch_weather(
            c.LOCATION, UnitSystem.IMPERIAL
        )
        assert weather_data_imperial.unit_system == UnitSystem.IMPERIAL
