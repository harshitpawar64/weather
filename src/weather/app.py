import asyncio

import httpx
import msgspec

from weather.cache import Cache
from weather.config import Config
from weather.models import Theme, UnitSystem, WeatherResponse
from weather.onboarding import onboarding
from weather.services import (
    AQIService,
    GeocodingService,
    GeolocationService,
    WeatherService,
)
from weather.ui.render import render_weather

cache = Cache()
config = Config()


async def run(
    query: str | None,
    unit_system: UnitSystem,
    theme: Theme,
    days: int,
    json_output: bool,
):
    async with httpx.AsyncClient(timeout=10.0) as client:
        if query:
            geocoder = GeocodingService(client, cache)
            location = await geocoder.geocode(query)
        elif config.location:
            location = config.location
        else:
            location, unit_system = await onboarding(
                GeolocationService(client), GeocodingService(client, cache)
            )

            config.save(location, unit_system)

        weather_service = WeatherService(client, cache)
        aqi_service = AQIService(client, cache)

        weather, aqi = await asyncio.gather(
            weather_service.get_weather(location, unit_system),
            aqi_service.get_aqi(location),
        )

    cache.save(location, weather, aqi, query)

    response = WeatherResponse(location, weather, aqi)

    if json_output:
        print(msgspec.json.encode(response).decode())

        return

    render_weather(response, theme, days)
