from datetime import UTC, datetime, timedelta

import pytest

import tests.constants as c
from weather.models import UnitSystem
from weather.ui.presentation import (
    aqi_category,
    format_day,
    format_precipitation,
    format_sun,
    format_temperature,
    format_updated,
    format_wind_speed,
    uvi_category,
    wind_direction,
)


@pytest.mark.parametrize(
    ("temp", "units", "expected_color"),
    [
        (-5.0, UnitSystem.METRIC, "cyan"),
        (0.0, UnitSystem.METRIC, "cyan"),
        (5.0, UnitSystem.METRIC, "bright_blue"),
        (10.0, UnitSystem.METRIC, "bright_blue"),
        (15.0, UnitSystem.METRIC, "green"),
        (20.0, UnitSystem.METRIC, "green"),
        (25.0, UnitSystem.METRIC, "yellow"),
        (30.0, UnitSystem.METRIC, "yellow"),
        (35.0, UnitSystem.METRIC, "dark_orange"),
        (40.0, UnitSystem.METRIC, "dark_orange"),
        (45.0, UnitSystem.METRIC, "red"),
        (32.0, UnitSystem.IMPERIAL, "cyan"),
        (68.0, UnitSystem.IMPERIAL, "green"),
    ],
)
def test_format_temperature_colors(
    temp: float, units: UnitSystem, expected_color: str
) -> None:
    result = format_temperature(temp, units)
    assert f"[{expected_color}]" in result


def test_format_temperature_none() -> None:
    assert format_temperature(None, UnitSystem.METRIC) == "[dim]-[/]"


@pytest.mark.parametrize(
    ("aqi", "expected_label"),
    [
        (25, "[Good]"),
        (50, "[Good]"),
        (75, "[Moderate]"),
        (100, "[Moderate]"),
        (125, "[Unhealthy for sensitive groups]"),
        (150, "[Unhealthy for sensitive groups]"),
        (175, "[Unhealthy]"),
        (200, "[Unhealthy]"),
        (250, "[Very unhealthy]"),
        (300, "[Very unhealthy]"),
        (400, "[Hazardous]"),
    ],
)
def test_aqi_category(aqi: float, expected_label: str) -> None:
    result = aqi_category(aqi)
    assert expected_label in result


@pytest.mark.parametrize(
    ("uvi", "expected_label"),
    [
        (1.0, "[Low]"),
        (2.0, "[Low]"),
        (3.0, "[Moderate]"),
        (5.0, "[Moderate]"),
        (6.0, "[High]"),
        (7.0, "[High]"),
        (8.0, "[Very high]"),
        (10.0, "[Very high]"),
        (11.0, "[Extreme]"),
        (15.0, "[Extreme]"),
    ],
)
def test_uvi_category(uvi: float, expected_label: str) -> None:
    result = uvi_category(uvi)
    assert expected_label in result


@pytest.mark.parametrize(
    ("degrees", "expected_arrow"),
    [
        (0, "↑"),
        (45, "↗"),
        (90, "→"),
        (135, "↘"),
        (180, "↓"),
        (225, "↙"),
        (270, "←"),
        (315, "↖"),
        (360, "↑"),
    ],
)
def test_wind_direction(degrees: int, expected_arrow: str) -> None:
    result = wind_direction(degrees)
    assert expected_arrow in result


def test_format_precipitation() -> None:
    assert format_precipitation(None) == "[dim]-[/]"
    assert format_precipitation(10) == "10%"
    assert "[cyan]45%[/]" == format_precipitation(45)
    assert "[bold cyan]80% ☂[/]" == format_precipitation(80)


def test_format_wind_speed_metric() -> None:
    assert format_wind_speed(None, UnitSystem.METRIC) == "[dim]-[/]"
    assert format_wind_speed(20.0, UnitSystem.METRIC) == "20 km/h"
    assert format_wind_speed(45.0, UnitSystem.METRIC) == "[bold yellow]45 km/h ⚠[/]"


def test_format_wind_speed_imperial() -> None:
    assert format_wind_speed(15.0, UnitSystem.IMPERIAL) == "15 mph"
    assert format_wind_speed(30.0, UnitSystem.IMPERIAL) == "[bold yellow]30 mph ⚠[/]"


def test_format_updated() -> None:
    now = datetime.now(UTC)

    just_now = now.isoformat()
    assert "just now" in format_updated(just_now)

    ten_mins_ago = (now - timedelta(minutes=10)).isoformat()
    assert "10m ago" in format_updated(ten_mins_ago)

    two_hours_ago = (now - timedelta(hours=2)).isoformat()
    assert "2h ago" in format_updated(two_hours_ago)

    two_days_ago = (now - timedelta(days=2)).isoformat()
    assert "2d ago" in format_updated(two_days_ago)

    assert format_updated("invalid_date") == "invalid_date"


def test_format_day() -> None:
    assert format_day(c.DATE) == "Thu 01 Jan"
    assert format_day("invalid_date") == "invalid_date"


def test_format_sun_standard() -> None:
    assert format_sun(c.SUNRISE, c.SUNSET) == "06:00 - 21:00"


def test_format_sun_polar_night() -> None:
    assert (
        format_sun("1970-01-01T00:00", "1970-01-01T00:00") == "[cyan]⏾ Polar night[/]"
    )


def test_format_sun_midnight_sun() -> None:
    assert (
        format_sun("1970-01-01T00:00", "1970-01-02T00:00")
        == "[yellow]☀ Midnight sun[/]"
    )
