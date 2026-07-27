import httpx

import tests.constants as c
from weather.providers.aqi import OpenMeteo
from weather.providers.aqi.openmeteo import OpenMeteoCurrentResponse
from weather.providers.aqi.openmeteo import OpenMeteoResponse as OpenMeteoAQIResponse


async def test_openmeteo_aqi_fetch():
    current_payload = OpenMeteoCurrentResponse(
        time="1970-01-01T00:00", interval=3600, us_aqi=42, pm10=18.5, pm2_5=9.2
    )
    payload = OpenMeteoAQIResponse(utc_offset_seconds=0, current=current_payload)

    transport = httpx.MockTransport(
        lambda req: httpx.Response(200, content=c.ENCODER.encode(payload))
    )

    async with httpx.AsyncClient(transport=transport) as client:
        provider = OpenMeteo(client)
        aqi_data = await provider.fetch_aqi(c.LOCATION)

        assert aqi_data.us_aqi == 42.0
        assert aqi_data.pm_2_5 == 9.2
        assert aqi_data.pm_10 == 18.5
