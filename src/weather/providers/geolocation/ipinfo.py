import msgspec

from weather.models import Location
from weather.providers.geolocation.base import GeolocationProvider


class IPInfoResponse(msgspec.Struct, frozen=True):
    loc: str
    city: str
    region: str
    postal: str
    country: str

    @property
    def coordinates(self) -> tuple[float, float]:
        latitude, longitude = self.loc.split(",")

        return float(latitude), float(longitude)


class IPInfo(GeolocationProvider):
    API_URL = "https://ipinfo.io"

    async def geolocate(self) -> Location:
        response = await self.client.get(self.API_URL)
        response.raise_for_status()

        data = msgspec.json.decode(response.content, type=IPInfoResponse)

        return self._parse_data(data)

    @staticmethod
    def _parse_data(data: IPInfoResponse) -> Location:
        latitude, longitude = data.coordinates
        display_name = f"{data.city}, {data.region}, {data.postal}, {data.country}"

        return Location(
            latitude=latitude, longitude=longitude, display_name=display_name
        )
