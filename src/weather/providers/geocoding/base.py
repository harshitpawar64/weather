from abc import abstractmethod

from weather.models import Location
from weather.providers import Provider


class GeocodingProvider(Provider):
    @abstractmethod
    async def geocode(self, query: str) -> Location: ...
