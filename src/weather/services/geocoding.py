import logging

import httpx

from weather.cache import Cache
from weather.models import Location
from weather.providers.geocoding import Nominatim, OpenMeteo

logger = logging.getLogger(__name__)


class GeocodingService:
    def __init__(self, client: httpx.AsyncClient, cache: Cache):
        self.providers = (Nominatim(client), OpenMeteo(client))
        self.cache = cache

    async def geocode(self, query: str) -> Location:
        if cached_data := self.cache.get_location(query):
            logger.info(f"Geocoding cache hit for query: '{query}'")
            return cached_data

        for provider in self.providers:
            try:
                return await provider.geocode(query)
            except Exception as e:
                logger.warning("%s failed: %s.", provider.__class__.__name__, e)

        logger.error("All geocoding providers failed.")
        raise RuntimeError("All geocoding providers failed.")
