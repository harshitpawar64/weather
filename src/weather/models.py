from enum import StrEnum, auto
from typing import NewType

import msgspec

UnixTimestamp = NewType("UnixTimestamp", float)


class UnitSystem(StrEnum):
    METRIC = auto()
    IMPERIAL = auto()

    @property
    def temperature(self) -> str:
        return "°C" if self == UnitSystem.METRIC else "°F"

    @property
    def wind_speed(self) -> str:
        return "km/h" if self == UnitSystem.METRIC else "mph"

    @property
    def precipitation(self) -> str:
        return "mm" if self == UnitSystem.METRIC else "in"


class Location(msgspec.Struct, frozen=True):
    latitude: float
    longitude: float
    display_name: str

    def __post_init__(self):
        if not -90 <= self.latitude <= 90:
            raise ValueError()
        if not -180 <= self.longitude <= 180:
            raise ValueError()


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
    weather_code: int
    temp_min: float
    temp_max: float
    precipitation_sum: float
    precipitation_prob_max: float
    wind_speed_max: float
    sunrise: str
    sunset: str


class AirQuality(msgspec.Struct, frozen=True):
    us_aqi: float
    pm_2_5: float
    pm_10: float
    valid_until: float


class WeatherData(msgspec.Struct, frozen=True):
    current: CurrentWeather
    daily: list[DailyForecast]
    unit_system: UnitSystem
    valid_until: UnixTimestamp
