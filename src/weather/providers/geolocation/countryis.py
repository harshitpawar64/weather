import msgspec

from weather.models import Location
from weather.providers.geolocation.base import GeolocationProvider


class CountryIsLocation(msgspec.Struct, frozen=True):
    latitude: float
    longitude: float


class CountryIsResponse(msgspec.Struct, frozen=True):
    location: CountryIsLocation
    city: str
    country: str


class CountryIs(GeolocationProvider):
    API_URL = "https://api.country.is"

    async def geolocate(self) -> Location:
        params = {"fields": "location,city,country"}

        response = await self.client.get(self.API_URL, params=params)
        response.raise_for_status()

        data = msgspec.json.decode(response.content, type=CountryIsResponse)

        return self._parse_data(data)

    @staticmethod
    def _parse_data(data: CountryIsResponse) -> Location:
        display_name = f"{data.city}, {data.country}"

        return Location(
            latitude=data.location.latitude,
            longitude=data.location.longitude,
            display_name=display_name,
        )
