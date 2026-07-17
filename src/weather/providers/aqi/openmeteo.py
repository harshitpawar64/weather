from datetime import datetime, timedelta, timezone
from typing import Any

import msgspec

from weather.models import AirQuality, Location, UnixTimestamp
from weather.providers.aqi.base import AQIProvider


class OpenMeteoCurrentResponse(msgspec.Struct, frozen=True):
    time: str
    interval: int
    us_aqi: int
    pm10: float
    pm2_5: float


class OpenMeteoResponse(msgspec.Struct, frozen=True):
    utc_offset_seconds: int
    current: OpenMeteoCurrentResponse


class OpenMeteo(AQIProvider):
    API_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

    async def fetch_aqi(self, location: Location) -> AirQuality:
        params: dict[str, Any] = {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "current": ["us_aqi", "pm2_5", "pm10"],
            "timezone": "auto",
        }

        response = await self.client.get(self.API_URL, params=params)
        response.raise_for_status()

        data = msgspec.json.decode(response.content, type=OpenMeteoResponse)

        return self._parse_data(data.current, self._valid_until(data))

    @staticmethod
    def _parse_data(
        current: OpenMeteoCurrentResponse, valid_until: UnixTimestamp
    ) -> AirQuality:
        return AirQuality(
            us_aqi=current.us_aqi,
            pm_2_5=current.pm2_5,
            pm_10=current.pm10,
            valid_until=valid_until,
        )

    @staticmethod
    def _valid_until(data: OpenMeteoResponse) -> UnixTimestamp:
        current = data.current
        utc_dt = datetime.fromisoformat(current.time).replace(
            tzinfo=timezone(timedelta(seconds=data.utc_offset_seconds))
        )

        return UnixTimestamp(utc_dt.timestamp() + current.interval)
