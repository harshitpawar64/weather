from abc import abstractmethod
from typing import ClassVar

from weather.models import Location, UnitSystem, WeatherData
from weather.providers import Provider


class WeatherProvider(Provider):
    API_URL: ClassVar[str]

    @abstractmethod
    async def fetch_weather(
        self, location: Location, unit_system: UnitSystem
    ) -> WeatherData: ...
