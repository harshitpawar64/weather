from abc import abstractmethod

from weather.models import Location
from weather.providers import Provider


class GeocodingProvider(Provider):
    API_URL: str

    @abstractmethod
    async def geocode(self, query: str) -> Location: ...
