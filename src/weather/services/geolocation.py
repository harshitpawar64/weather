import logging

import httpx

from weather.models import Location
from weather.providers.geolocation import FreeIPAPI, IPInfo, IPWhoIs

logger = logging.getLogger(__name__)


class GeolocationService:
    def __init__(self, client: httpx.AsyncClient):
        self.providers = (IPWhoIs(client), FreeIPAPI(client), IPInfo(client))

    async def geolocate(self) -> Location:
        for provider in self.providers:
            try:
                return await provider.geolocate()
            except Exception as e:
                logger.warning(f"{provider.__class__.__name__} failed: {e}.")

        raise RuntimeError("All geolocation providers failed.")
