from abc import abstractmethod

from weather.models import Location
from weather.providers import Provider


class GeolocationProvider(Provider):
    API_URL: str

    @abstractmethod
    async def geolocate(self) -> Location: ...
