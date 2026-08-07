from datetime import datetime
from typing import Any

import msgspec

from weather.models import (
    CurrentWeather,
    DailyForecast,
    Location,
    UnitSystem,
    WeatherData,
)
from weather.providers.weather import WeatherProvider
from weather.utils import calculate_valid_until, parse_datetime


class OpenMeteoCurrentResponse(msgspec.Struct, frozen=True):
    time: str
    interval: int
    weather_code: int
    temperature_2m: float
    apparent_temperature: float
    relative_humidity_2m: int
    precipitation: float
    wind_speed_10m: float
    wind_direction_10m: int
    wind_gusts_10m: float
    is_day: int


class OpenMeteoDailyResponse(msgspec.Struct, frozen=True):
    time: list[str]
    weather_code: list[int | None]
    temperature_2m_min: list[float | None]
    temperature_2m_max: list[float | None]
    precipitation_sum: list[float | None]
    precipitation_probability_max: list[int | None]
    wind_speed_10m_max: list[float | None]
    sunrise: list[str]
    sunset: list[str]


class OpenMeteoResponse(msgspec.Struct, frozen=True):
    utc_offset_seconds: int
    current: OpenMeteoCurrentResponse
    daily: OpenMeteoDailyResponse


class OpenMeteo(WeatherProvider):
    API_URL = "https://api.open-meteo.com/v1/forecast"

    async def fetch_weather(
        self, location: Location, unit_system: UnitSystem
    ) -> WeatherData:
        params: dict[str, Any] = {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "current": [
                "weather_code",
                "temperature_2m",
                "apparent_temperature",
                "relative_humidity_2m",
                "precipitation",
                "wind_speed_10m",
                "wind_direction_10m",
                "wind_gusts_10m",
                "is_day",
            ],
            "daily": [
                "temperature_2m_min",
                "temperature_2m_max",
                "precipitation_sum",
                "precipitation_probability_max",
                "wind_speed_10m_max",
                "sunrise",
                "sunset",
                "weather_code",
            ],
            "forecast_days": 16,
            "timezone": "auto",
        }

        if unit_system is UnitSystem.IMPERIAL:
            params["temperature_unit"] = "fahrenheit"
            params["wind_speed_unit"] = "mph"
            params["precipitation_unit"] = "inch"

        response = await self.client.get(self.API_URL, params=params)
        response.raise_for_status()

        data = msgspec.json.decode(response.content, type=OpenMeteoResponse)

        local_dt = parse_datetime(data.current.time, data.utc_offset_seconds)

        return WeatherData(
            current=self._parse_current(data.current, local_dt),
            daily=self._parse_daily(data.daily),
            unit_system=unit_system,
            valid_until=calculate_valid_until(local_dt, data.current.interval),
        )

    @staticmethod
    def _parse_current(
        current: OpenMeteoCurrentResponse, utc_dt: datetime
    ) -> CurrentWeather:
        return CurrentWeather(
            time=utc_dt.isoformat(),
            weather_code=current.weather_code,
            temperature=current.temperature_2m,
            apparent_temperature=current.apparent_temperature,
            humidity=current.relative_humidity_2m,
            precipitation=current.precipitation,
            wind_speed=current.wind_speed_10m,
            wind_direction=current.wind_direction_10m,
            wind_gusts=current.wind_gusts_10m,
            is_day=bool(current.is_day),
        )

    @staticmethod
    def _parse_daily(daily: OpenMeteoDailyResponse) -> list[DailyForecast]:
        rows = zip(
            daily.time,
            daily.weather_code,
            daily.temperature_2m_min,
            daily.temperature_2m_max,
            daily.precipitation_sum,
            daily.precipitation_probability_max,
            daily.wind_speed_10m_max,
            daily.sunrise,
            daily.sunset,
        )

        return [DailyForecast(*row) for row in rows]
