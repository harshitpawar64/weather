from enum import StrEnum, auto
from typing import NewType

import msgspec

UnixTimestamp = NewType("UnixTimestamp", float)


class UnitSystem(StrEnum):
    METRIC = auto()
    IMPERIAL = auto()

    @property
    def temperature(self) -> str:
        return "°C" if self is UnitSystem.METRIC else "°F"

    @property
    def wind_speed(self) -> str:
        return "km/h" if self is UnitSystem.METRIC else "mph"

    @property
    def precipitation(self) -> str:
        return "mm" if self is UnitSystem.METRIC else "in"

    @property
    def symbols(self) -> str:
        return f"{self.temperature}, {self.wind_speed}, {self.precipitation}"

    @property
    def label(self) -> str:
        return f"{self} ({self.symbols})"


class Theme(StrEnum):
    DEFAULT = auto()


class Location(msgspec.Struct, frozen=True):
    latitude: float
    longitude: float
    display_name: str

    def __post_init__(self):
        if not -90 <= self.latitude <= 90:
            raise msgspec.ValidationError(f"Invalid latitude: {self.latitude}")
        if not -180 <= self.longitude <= 180:
            raise msgspec.ValidationError(f"Invalid longitude: {self.longitude}")


class CurrentWeather(msgspec.Struct, frozen=True):
    time: str
    weather_code: int
    temperature: float
    apparent_temperature: float
    humidity: int
    precipitation: float
    wind_speed: float
    wind_direction: int
    wind_gusts: float
    is_day: bool


class DailyForecast(msgspec.Struct, frozen=True):
    date: str
    weather_code: int | None
    temp_min: float | None
    temp_max: float | None
    precipitation_sum: float | None
    precipitation_prob_max: int | None
    wind_speed_max: float | None
    sunrise: str
    sunset: str


class AirQuality(msgspec.Struct, frozen=True):
    us_aqi: float
    pm_2_5: float
    pm_10: float
    uv_index: float | None
    valid_until: UnixTimestamp


class WeatherData(msgspec.Struct, frozen=True):
    current: CurrentWeather
    daily: list[DailyForecast]
    unit_system: UnitSystem
    valid_until: UnixTimestamp


class WeatherResponse(msgspec.Struct, frozen=True):
    location: Location
    weather: WeatherData
    aqi: AirQuality | None
