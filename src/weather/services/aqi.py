import logging

import httpx

from weather.models import AirQuality, Location
from weather.providers.aqi import OpenMeteo

logger = logging.getLogger(__name__)


class AQIService:
    def __init__(self, client: httpx.AsyncClient):
        self.providers = (OpenMeteo(client),)

    async def get_aqi(self, location: Location) -> AirQuality:
        for provider in self.providers:
            try:
                return await provider.fetch_aqi(location)
            except Exception as e:
                logger.warning(f"{provider.__class__.__name__} failed: {e}.")

        raise RuntimeError("All AQI providers failed.")
