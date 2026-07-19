import msgspec

from weather.models import Location
from weather.providers.geocoding.base import GeocodingProvider


class OpenMeteoResultResponse(msgspec.Struct, frozen=True):
    latitude: float
    longitude: float
    name: str
    admin4: str = ""
    admin3: str = ""
    admin2: str = ""
    admin1: str = ""
    country: str = ""


class OpenMeteoResponse(msgspec.Struct, frozen=True):
    results: list[OpenMeteoResultResponse] = []


class OpenMeteo(GeocodingProvider):
    API_URL = "https://geocoding-api.open-meteo.com/v1/search"

    async def geocode(self, query: str) -> Location:
        params: dict[str, str | int] = {"name": query, "format": "json", "count": 1}

        response = await self.client.get(self.API_URL, params=params)
        response.raise_for_status()

        data = msgspec.json.decode(response.content, type=OpenMeteoResponse)

        if not data.results:
            raise ValueError(f"No location found for query: '{query}'")

        return self._parse_data(data.results[0])

    @staticmethod
    def _parse_data(result: OpenMeteoResultResponse) -> Location:
        parts = (
            result.name,
            result.admin4,
            result.admin3,
            result.admin2,
            result.admin1,
            result.country,
        )

        display_name = ", ".join(dict.fromkeys(filter(None, parts)))

        return Location(
            latitude=result.latitude,
            longitude=result.longitude,
            display_name=display_name,
        )
