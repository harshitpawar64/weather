import asyncio

import httpx
from rich.console import Console

from weather.cache import Cache
from weather.models import UnitSystem
from weather.services import (
    AQIService,
    GeocodingService,
    GeolocationService,
    WeatherService,
)

console = Console()
cache = Cache()


async def run(query: str | None, unit_system: UnitSystem):
    async with httpx.AsyncClient(timeout=10.0) as client:
        if query:
            geocoder = GeocodingService(client, cache)
            location = await geocoder.geocode(query)
        else:
            geolocator = GeolocationService(client)
            location = await geolocator.geolocate()

        weather_service = WeatherService(client, cache)
        aqi_service = AQIService(client, cache)

        weather, aqi = await asyncio.gather(
            weather_service.get_weather(location, unit_system),
            aqi_service.get_aqi(location),
        )

    cache.save(location, weather, aqi)

    console.print(location)
    console.print(weather)
    console.print(aqi)
