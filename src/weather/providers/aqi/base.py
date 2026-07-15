from abc import abstractmethod

from weather.models import AirQuality, Location
from weather.providers import Provider


class AQIProvider(Provider):
    API_URL: str

    @abstractmethod
    async def fetch_aqi(self, location: Location) -> AirQuality: ...
