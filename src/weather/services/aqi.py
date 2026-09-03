import logging

import httpx
import msgspec

from weather.cache import Cache
from weather.exceptions import ProviderError, ServiceError
from weather.models import AirQuality, Location
from weather.providers.aqi import AQIProvider, OpenMeteo, OpenWeather

logger = logging.getLogger(__name__)


class AQIService:
    def __init__(self, client: httpx.AsyncClient, cache: Cache) -> None:
        self.providers: tuple[AQIProvider, ...] = (
            OpenMeteo(client),
            OpenWeather(client),
        )
        self.cache = cache

    async def get_aqi(self, location: Location) -> AirQuality:
        if cached_data := self.cache.get_aqi(location):
            logger.info(
                "AQI cache hit for coordinates: (%s, %s)",
                location.latitude,
                location.longitude,
            )
            return cached_data

        for provider in self.providers:
            if not provider.is_configured:
                continue
            try:
                return await provider.fetch_aqi(location)
            except (httpx.HTTPError, msgspec.DecodeError, ProviderError) as e:
                logger.warning("%s failed: %s.", provider.__class__.__name__, e)

        if stale_cache := self.cache.get_aqi(location, ignore_expiry=True):
            return stale_cache

        raise ServiceError("All AQI providers failed.")
