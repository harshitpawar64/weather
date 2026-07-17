from abc import abstractmethod
from typing import ClassVar

from weather.models import Location
from weather.providers import Provider


class GeocodingProvider(Provider):
    API_URL: ClassVar[str]

    @abstractmethod
    async def geocode(self, query: str) -> Location: ...
