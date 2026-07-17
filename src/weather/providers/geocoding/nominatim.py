import msgspec

from weather import __version__
from weather.models import Location
from weather.providers.geocoding.base import GeocodingProvider


class NominatimResponse(msgspec.Struct, frozen=True):
    lat: str
    lon: str
    display_name: str


class Nominatim(GeocodingProvider):
    API_URL = "https://nominatim.openstreetmap.org/search"

    async def geocode(self, query: str) -> Location:
        params: dict[str, str | int] = {
            "q": query,
            "format": "jsonv2",
            "layer": "address,natural,railway,manmade",
            "limit": 1,
        }

        headers = {"User-Agent": f"weather/{__version__}", "Accept-Language": "en"}

        response = await self.client.get(self.API_URL, params=params, headers=headers)
        response.raise_for_status()

        data = msgspec.json.decode(response.content, type=list[NominatimResponse])

        if not data:
            raise ValueError(f"No location found for query: '{query}'")

        return self._parse_data(data[0])

    @staticmethod
    def _parse_data(data: NominatimResponse) -> Location:
        return Location(
            latitude=float(data.lat),
            longitude=float(data.lon),
            display_name=data.display_name,
        )
