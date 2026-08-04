from datetime import datetime, timedelta, timezone

from weather.models import UnixTimestamp
from weather.utils import calculate_valid_until, get_us_aqi, parse_datetime


def test_parse_datetime_utc():
    dt = parse_datetime("1970-01-01T00:00", 0)
    assert dt.year == 1970
    assert dt.month == 1
    assert dt.day == 1
    assert dt.hour == 0
    assert dt.minute == 0
    assert dt.tzinfo == timezone.utc


def test_parse_datetime_positive_offset():
    dt = parse_datetime("1970-01-01T00:00", 3600)
    assert dt.utcoffset() == timedelta(seconds=3600)


def test_parse_datetime_negative_offset():
    dt = parse_datetime("1970-01-01T00:00", -3600)
    assert dt.utcoffset() == timedelta(seconds=-3600)


def test_calculate_valid_until():
    dt = datetime(1970, 1, 1, tzinfo=timezone.utc)
    assert calculate_valid_until(dt, 3600) == UnixTimestamp(3600.0)


def test_calculate_valid_until_zero_interval():
    dt = datetime(1970, 1, 1, tzinfo=timezone.utc)
    assert calculate_valid_until(dt, 0) == UnixTimestamp(0.0)


def test_get_us_aqi_zero():
    assert get_us_aqi(0.0, 0.0) == 0


def test_get_us_aqi_good_pm25_dominates():
    assert get_us_aqi(5.0, 25.0) == 28


def test_get_us_aqi_moderate_pm25_dominates():
    assert get_us_aqi(10.0, 10.0) == 53


def test_get_us_aqi_pm10_dominates():
    assert get_us_aqi(0.0, 100.0) == 73


def test_get_us_aqi_hazardous():
    assert get_us_aqi(350.0, 0.0) == 415
