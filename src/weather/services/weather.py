import logging

import httpx

from weather.models import Location, UnitSystem, WeatherData
from weather.providers.weather import OpenMeteo

logger = logging.getLogger(__name__)


class WeatherService:
    def __init__(self, client: httpx.AsyncClient):
        self.providers = (OpenMeteo(client),)

    async def get_weather(
        self, location: Location, unit_system: UnitSystem
    ) -> WeatherData:
        for provider in self.providers:
            try:
                return await provider.fetch_weather(location, unit_system)
            except Exception as e:
                logger.warning(f"{provider.__class__.__name__} failed: {e}")

        raise RuntimeError("All Weather providers failed.")
