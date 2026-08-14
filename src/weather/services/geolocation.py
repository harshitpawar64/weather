import logging

import httpx
import msgspec

from weather.exceptions import ProviderError, ServiceError
from weather.models import Location
from weather.providers.geolocation import (
    CountryIs,
    FreeIPAPI,
    GeolocationProvider,
    IPInfo,
    IPWhoIs,
)

logger = logging.getLogger(__name__)


class GeolocationService:
    def __init__(self, client: httpx.AsyncClient):
        self.providers: tuple[GeolocationProvider, ...] = (
            IPWhoIs(client),
            FreeIPAPI(client),
            CountryIs(client),
            IPInfo(client),
        )

    async def geolocate(self) -> Location:
        for provider in self.providers:
            if not provider.is_configured:
                continue
            try:
                return await provider.geolocate()
            except (httpx.HTTPError, msgspec.DecodeError, ProviderError) as e:
                logger.warning("%s failed: %s.", provider.__class__.__name__, e)

        logger.error("All geolocation providers failed.")
        raise ServiceError("All geolocation providers failed.")
