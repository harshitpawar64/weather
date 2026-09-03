import logging

import httpx
import msgspec

from weather.cache import Cache
from weather.exceptions import ProviderError, ServiceError
from weather.models import Location
from weather.providers.geocoding import GeocodingProvider, Nominatim, OpenMeteo

logger = logging.getLogger(__name__)


class GeocodingService:
    def __init__(self, client: httpx.AsyncClient, cache: Cache) -> None:
        self.providers: tuple[GeocodingProvider, ...] = (
            Nominatim(client),
            OpenMeteo(client),
        )
        self.cache = cache

    async def geocode(self, query: str) -> Location:
        if cached_data := self.cache.get_location(query):
            logger.info("Geocoding cache hit for query: '%s'", query)
            return cached_data

        for provider in self.providers:
            if not provider.is_configured:
                continue
            try:
                return await provider.geocode(query)
            except (httpx.HTTPError, msgspec.DecodeError, ProviderError) as e:
                logger.warning("%s failed: %s.", provider.__class__.__name__, e)

        raise ServiceError("All geocoding providers failed.")
