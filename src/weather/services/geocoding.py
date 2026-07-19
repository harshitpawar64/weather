import logging

import httpx

from weather.models import Location
from weather.providers.geocoding import Nominatim, OpenMeteo

logger = logging.getLogger(__name__)


class GeocodingService:
    def __init__(self, client: httpx.AsyncClient):
        self.providers = (Nominatim(client), OpenMeteo(client))

    async def geocode(self, query: str) -> Location:
        for provider in self.providers:
            try:
                return await provider.geocode(query)
            except Exception as e:
                logger.warning(f"{provider.__class__.__name__} failed: {e}.")

        raise RuntimeError("All geocoding providers failed.")
