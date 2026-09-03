import logging
import time
from pathlib import Path

import msgspec
from platformdirs import user_cache_path

from weather.models import AirQuality, Location, UnitSystem, WeatherData

logger = logging.getLogger(__name__)

_STALE_MAX_AGE = 604800  # 1 week


class CacheEntry(msgspec.Struct, frozen=True):
    weather: WeatherData | None = None
    aqi: AirQuality | None = None


class CacheData(msgspec.Struct):
    queries: dict[str, Location] = {}
    data: dict[str, CacheEntry] = {}


class Cache:
    def __init__(self, cache_dir: Path | None = None) -> None:
        self.file = (
            cache_dir or user_cache_path("weather", ensure_exists=True)
        ) / "cache.bin"

        self._encoder = msgspec.msgpack.Encoder()
        self._decoder = msgspec.msgpack.Decoder(type=CacheData)

        self._data = self._read()

    def _read(self) -> CacheData:
        try:
            return self._decoder.decode(self.file.read_bytes())
        except FileNotFoundError:
            logger.info(
                "Cache file not found at '%s'. Creating a new cache file...", self.file
            )
        except msgspec.DecodeError:
            logger.info(
                "Cache file at '%s' is corrupted. Resetting cache...", self.file
            )

        return CacheData()

    def _write(self) -> None:
        try:
            temp_file = self.file.with_suffix(".tmp")
            temp_file.write_bytes(self._encoder.encode(self._data))
            temp_file.replace(self.file)
        except OSError as e:
            temp_file.unlink(missing_ok=True)
            logger.warning("Failed to write cache file to '%s': %s", self.file, e)

    def get_location(self, query: str) -> Location | None:
        return self._data.queries.get(query.strip().lower())

    def get_weather(
        self, location: Location, unit_system: UnitSystem, ignore_expiry: bool = False
    ) -> WeatherData | None:
        key = self._get_key(location)
        entry = self._data.data.get(key)

        if not entry or not entry.weather:
            return None

        if entry.weather.unit_system != unit_system:
            return None

        if not ignore_expiry and time.time() > entry.weather.valid_until:
            return None

        return entry.weather

    def get_aqi(
        self, location: Location, ignore_expiry: bool = False
    ) -> AirQuality | None:
        key = self._get_key(location)

        entry = self._data.data.get(key)

        if not entry or not entry.aqi:
            return None

        if not ignore_expiry and time.time() > entry.aqi.valid_until:
            return None

        return entry.aqi

    def save(
        self,
        location: Location,
        weather: WeatherData,
        aqi: AirQuality | None = None,
        query: str | None = None,
    ) -> None:
        if query:
            self._data.queries[query.strip().lower()] = location

        key = self._get_key(location)

        self._data.data[key] = CacheEntry(weather=weather, aqi=aqi)

        removed = self.prune()

        if not removed:
            self._write()

    def prune(self) -> int:
        now = time.time()

        stale_keys = [
            key
            for key, entry in self._data.data.items()
            if (not entry.weather or now > entry.weather.valid_until + _STALE_MAX_AGE)
            and (not entry.aqi or now > entry.aqi.valid_until + _STALE_MAX_AGE)
        ]

        if not stale_keys:
            return 0

        for key in stale_keys:
            del self._data.data[key]

        self._write()

        return len(stale_keys)

    def clear(self) -> None:
        self.file.unlink(missing_ok=True)
        self.file.with_suffix(".tmp").unlink(missing_ok=True)

    @staticmethod
    def _get_key(location: Location) -> str:
        return f"{round(location.latitude, 2)},{round(location.longitude, 2)}"
