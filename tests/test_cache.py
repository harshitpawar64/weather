import time
from collections.abc import Callable
from pathlib import Path
from unittest.mock import MagicMock

import pytest

import tests.constants as c
from weather.cache import Cache, CacheEntry
from weather.models import AirQuality, UnitSystem, UnixTimestamp, WeatherData


def test_location_indexing(
    cache: Cache, make_weather: Callable[..., WeatherData]
) -> None:
    weather_data = make_weather(valid_until=time.time() + 3600)
    cache.save(location=c.LOCATION, weather=weather_data, query="  San Francisco  ")

    assert cache.get_location("san francisco") == c.LOCATION
    assert cache.get_location("SAN FRANCISCO") == c.LOCATION
    assert cache.get_location("nonexistent") is None


def test_weather_hit_and_expiry(
    cache: Cache, make_weather: Callable[..., WeatherData]
) -> None:
    fresh_weather = make_weather(valid_until=time.time() + 3600)
    cache.save(location=c.LOCATION, weather=fresh_weather)

    assert cache.get_weather(c.LOCATION, UnitSystem.METRIC) == fresh_weather

    expired_weather = make_weather(valid_until=time.time() - 3600)
    cache.save(location=c.LOCATION, weather=expired_weather)

    assert cache.get_weather(c.LOCATION, UnitSystem.METRIC, ignore_expiry=False) is None
    assert (
        cache.get_weather(c.LOCATION, UnitSystem.METRIC, ignore_expiry=True)
        == expired_weather
    )


def test_unit_system_filtering(
    cache: Cache, make_weather: Callable[..., WeatherData]
) -> None:
    metric_weather = make_weather(
        valid_until=time.time() + 3600, unit_system=UnitSystem.METRIC
    )
    cache.save(location=c.LOCATION, weather=metric_weather)

    assert cache.get_weather(c.LOCATION, UnitSystem.METRIC) == metric_weather
    assert cache.get_weather(c.LOCATION, UnitSystem.IMPERIAL) is None


def test_aqi_hit_and_expiry(
    cache: Cache,
    make_weather: Callable[..., WeatherData],
    make_aqi: Callable[..., AirQuality],
) -> None:
    fresh_aqi = make_aqi(valid_until=time.time() + 3600)
    weather_dummy = make_weather(valid_until=time.time() + 3600)
    cache.save(location=c.LOCATION, weather=weather_dummy, aqi=fresh_aqi)

    assert cache.get_aqi(c.LOCATION) == fresh_aqi

    expired_aqi = make_aqi(valid_until=time.time() - 3600)
    cache.save(location=c.LOCATION, weather=weather_dummy, aqi=expired_aqi)

    assert cache.get_aqi(c.LOCATION, ignore_expiry=False) is None
    assert cache.get_aqi(c.LOCATION, ignore_expiry=True) == expired_aqi


def test_prune_entries(
    cache: Cache,
    make_weather: Callable[..., WeatherData],
    make_aqi: Callable[..., AirQuality],
) -> None:
    now = time.time()
    stale_timestamp = UnixTimestamp(now - 700000)  # > 1 week old

    stale_weather = make_weather(valid_until=stale_timestamp)
    stale_aqi = make_aqi(valid_until=stale_timestamp)
    key = cache._get_key(c.LOCATION)
    cache._data.data[key] = CacheEntry(weather=stale_weather, aqi=stale_aqi)

    pruned_count = cache.prune()
    assert pruned_count == 1
    assert cache.get_weather(c.LOCATION, UnitSystem.METRIC, ignore_expiry=True) is None

    assert cache.prune() == 0


def test_read_corrupted_file(tmp_path: Path) -> None:
    cache_file = tmp_path / "cache.bin"
    cache_file.write_bytes(b"\x80\xff\x00\x01INVALID_MSGPACK")

    cache = Cache(cache_dir=tmp_path)
    assert cache.get_weather(c.LOCATION, UnitSystem.METRIC) is None


def test_clear(cache: Cache, make_weather: Callable[..., WeatherData]) -> None:
    weather_data = make_weather(valid_until=time.time() + 3600)
    cache.save(location=c.LOCATION, weather=weather_data)
    assert cache.file.exists()

    cache.clear()
    assert not cache.file.exists()


def test_write_error(
    cache: Cache,
    make_weather: Callable[..., WeatherData],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    weather_data = make_weather(valid_until=time.time() + 3600)

    monkeypatch.setattr(
        Path, "write_bytes", MagicMock(side_effect=OSError("Permission denied"))
    )
    cache.save(location=c.LOCATION, weather=weather_data)
