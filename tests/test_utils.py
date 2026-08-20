from datetime import UTC, datetime, timedelta

import tests.constants as c
from weather.models import UnixTimestamp
from weather.utils import calculate_valid_until, get_us_aqi, parse_datetime


def test_parse_datetime_utc() -> None:
    dt = parse_datetime(c.TIME, 0)
    assert dt.year == 1970
    assert dt.month == 1
    assert dt.day == 1
    assert dt.hour == 0
    assert dt.minute == 0
    assert dt.tzinfo == UTC


def test_parse_datetime_positive_offset() -> None:
    dt = parse_datetime(c.TIME, 3600)
    assert dt.utcoffset() == timedelta(seconds=3600)


def test_parse_datetime_negative_offset() -> None:
    dt = parse_datetime(c.TIME, -3600)
    assert dt.utcoffset() == timedelta(seconds=-3600)


def test_calculate_valid_until() -> None:
    dt = datetime(1970, 1, 1, tzinfo=UTC)
    assert calculate_valid_until(dt, 3600) == UnixTimestamp(3600.0)


def test_calculate_valid_until_zero_interval() -> None:
    dt = datetime(1970, 1, 1, tzinfo=UTC)
    assert calculate_valid_until(dt, 0) == UnixTimestamp(0.0)


def test_get_us_aqi_zero() -> None:
    assert get_us_aqi(0.0, 0.0) == 0


def test_get_us_aqi_good_pm25_dominates() -> None:
    assert get_us_aqi(5.0, 25.0) == 28


def test_get_us_aqi_moderate_pm25_dominates() -> None:
    assert get_us_aqi(10.0, 10.0) == 53


def test_get_us_aqi_pm10_dominates() -> None:
    assert get_us_aqi(0.0, 100.0) == 73


def test_get_us_aqi_hazardous() -> None:
    assert get_us_aqi(350.0, 0.0) == 415


def test_get_us_aqi_exceeding_breakpoints() -> None:
    assert get_us_aqi(600.0, 700.0) > 500
