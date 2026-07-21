import logging

import httpx

from weather.cache import Cache
from weather.models import AirQuality, Location
from weather.providers.aqi import OpenMeteo

logger = logging.getLogger(__name__)


class AQIService:
    def __init__(self, client: httpx.AsyncClient, cache: Cache):
        self.providers = (OpenMeteo(client),)
        self.cache = cache

    async def get_aqi(self, location: Location) -> AirQuality:
        if cached_data := self.cache.get_aqi(location):
            logger.info(
                f"AQI cache hit for coordinates: ({location.latitude}, {location.longitude})"
            )
            return cached_data

        for provider in self.providers:
            try:
                return await provider.fetch_aqi(location)
            except Exception as e:
                logger.warning(f"{provider.__class__.__name__} failed: {e}.")

        if stale_cache := self.cache.get_aqi(location, ignore_expiry=True):
            return stale_cache

        raise RuntimeError("All AQI providers failed.")
