from abc import abstractmethod
from typing import ClassVar

from weather.models import Location
from weather.providers import Provider


class GeolocationProvider(Provider):
    API_URL: ClassVar[str]

    @abstractmethod
    async def geolocate(self) -> Location: ...
