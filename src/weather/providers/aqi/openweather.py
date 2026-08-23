from typing import Any, override

import msgspec

from weather.exceptions import ProviderError
from weather.models import AirQuality, Location, UnixTimestamp
from weather.providers.aqi.base import AQIProvider
from weather.utils import get_us_aqi


class OpenWeatherComponents(msgspec.Struct, frozen=True):
    pm2_5: float
    pm10: float


class OpenWeatherList(msgspec.Struct, frozen=True):
    dt: UnixTimestamp
    components: OpenWeatherComponents


class OpenWeatherResponse(msgspec.Struct, frozen=True):
    items: list[OpenWeatherList] = msgspec.field(name="list")


class OpenWeather(AQIProvider):
    API_URL = "https://api.openweathermap.org/data/2.5/air_pollution"
    API_KEY_ENV = "OPENWEATHER_API_KEY"

    @override
    async def fetch_aqi(self, location: Location) -> AirQuality:
        params: dict[str, Any] = {
            "lat": location.latitude,
            "lon": location.longitude,
            "appid": self.required_api_key,
        }

        response = await self.client.get(self.API_URL, params=params)
        response.raise_for_status()

        data = msgspec.json.decode(response.content, type=OpenWeatherResponse)

        if not data.items:
            raise ProviderError("No AQI data returned from OpenWeather.")

        return self._parse_data(data.items[0])

    @staticmethod
    def _parse_data(data: OpenWeatherList) -> AirQuality:
        us_aqi = get_us_aqi(data.components.pm2_5, data.components.pm10)

        return AirQuality(
            us_aqi=us_aqi,
            pm_2_5=data.components.pm2_5,
            pm_10=data.components.pm10,
            valid_until=UnixTimestamp(data.dt + 3600),
        )
