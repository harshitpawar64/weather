import time

import msgspec
from platformdirs import user_cache_path

from weather.models import AirQuality, Location, UnitSystem, WeatherData

_CACHE_DIR = user_cache_path("weather", "Harshit Pawar")
_CACHE_DIR.mkdir(parents=True, exist_ok=True)


class CacheEntry(msgspec.Struct, frozen=True):
    weather: WeatherData | None = None
    aqi: AirQuality | None = None


class CacheData(msgspec.Struct):
    queries: dict[str, Location] = {}
    data: dict[str, CacheEntry] = {}


class Cache:
    def __init__(self):
        self.file = _CACHE_DIR / "cache.bin"

        self._encoder = msgspec.msgpack.Encoder()
        self._decoder = msgspec.msgpack.Decoder(type=CacheData)

        self._data = self._read()

    def _read(self) -> CacheData:
        try:
            return self._decoder.decode(self.file.read_bytes())
        except FileNotFoundError, msgspec.ValidationError, msgspec.DecodeError:
            return CacheData()

    def get_location(self, query: str) -> Location | None:
        return self._data.queries.get(query.lower())

    def get_weather(
        self, location: Location, unit_system: UnitSystem
    ) -> WeatherData | None:
        key = self._get_key(location)
        entry = self._data.data.get(key)

        if not entry or not entry.weather:
            return None

        if entry.weather.unit_system != unit_system:
            return None

        if time.time() > entry.weather.valid_until:
            return None

        return entry.weather

    def get_aqi(self, location: Location) -> AirQuality | None:
        key = self._get_key(location)

        entry = self._data.data.get(key)

        if not entry or not entry.aqi:
            return None

        if time.time() > entry.aqi.valid_until:
            return None

        return entry.aqi

    def save(
        self,
        location: Location,
        weather: WeatherData,
        aqi: AirQuality,
        query: str | None = None,
    ) -> None:
        if query:
            self._data.queries[query.strip().lower()] = location

        key = self._get_key(location)

        self._data.data[key] = CacheEntry(weather=weather, aqi=aqi)

        self.file.write_bytes(self._encoder.encode(self._data))

    @staticmethod
    def _get_key(location: Location) -> str:
        return f"{round(location.latitude, 2)},{round(location.longitude, 2)}"
