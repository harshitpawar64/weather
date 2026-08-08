from abc import abstractmethod

from weather.models import AirQuality, Location
from weather.providers import Provider


class AQIProvider(Provider):
    @abstractmethod
    async def fetch_aqi(self, location: Location) -> AirQuality: ...
