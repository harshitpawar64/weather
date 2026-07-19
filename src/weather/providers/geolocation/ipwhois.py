import msgspec

from weather.models import Location
from weather.providers.geolocation.base import GeolocationProvider


class IPWhoIsResponse(msgspec.Struct, frozen=True):
    latitude: float
    longitude: float
    city: str
    region: str
    country: str


class IPWhoIs(GeolocationProvider):
    API_URL = "https://ipwho.is"

    async def geolocate(self) -> Location:
        params = {"fields": "latitude,longitude,city,region,country,postal"}

        response = await self.client.get(self.API_URL, params=params)
        response.raise_for_status()

        data = msgspec.json.decode(response.content, type=IPWhoIsResponse)

        return self._parse_data(data)

    @staticmethod
    def _parse_data(data: IPWhoIsResponse) -> Location:
        display_name = f"{data.city}, {data.region}, {data.country}"

        return Location(
            latitude=data.latitude, longitude=data.longitude, display_name=display_name
        )
