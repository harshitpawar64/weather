import msgspec

from weather.models import Location
from weather.providers.geolocation.base import GeolocationProvider


class FreeIPAPIResponse(msgspec.Struct, frozen=True):
    latitude: float
    longitude: float
    cityName: str
    regionName: str
    countryName: str


class FreeIPAPI(GeolocationProvider):
    API_URL = "https://free.freeipapi.com/api/json/"

    async def geolocate(self) -> Location:
        response = await self.client.get(self.API_URL)
        response.raise_for_status()

        data = msgspec.json.decode(response.content, type=FreeIPAPIResponse)

        return self._parse_data(data)

    @staticmethod
    def _parse_data(data: FreeIPAPIResponse) -> Location:
        display_name = f"{data.cityName}, {data.regionName}, {data.countryName}"

        return Location(
            latitude=data.latitude, longitude=data.longitude, display_name=display_name
        )
