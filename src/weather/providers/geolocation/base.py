from abc import abstractmethod

from weather.models import Location
from weather.providers import Provider


class GeolocationProvider(Provider):
    @abstractmethod
    async def geolocate(self) -> Location: ...
