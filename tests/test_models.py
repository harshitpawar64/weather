import msgspec
import pytest

import tests.constants as c
from weather.models import Location, UnitSystem


def test_unit_system_metric() -> None:
    unit = UnitSystem.METRIC
    assert unit.temperature == "°C"
    assert unit.wind_speed == "km/h"
    assert unit.precipitation == "mm"
    assert unit.symbols == "°C, km/h, mm"
    assert unit.label == "metric (°C, km/h, mm)"


def test_unit_system_imperial() -> None:
    unit = UnitSystem.IMPERIAL
    assert unit.temperature == "°F"
    assert unit.wind_speed == "mph"
    assert unit.precipitation == "in"
    assert unit.symbols == "°F, mph, in"
    assert unit.label == "imperial (°F, mph, in)"


def test_location_valid() -> None:
    location = c.LOCATION
    assert location.latitude == c.LATITUDE
    assert location.longitude == c.LONGITUDE
    assert location.display_name == c.DISPLAY_NAME


def test_location_invalid_latitude() -> None:
    with pytest.raises(msgspec.ValidationError, match="Invalid latitude"):
        Location(latitude=91.0, longitude=0.0, display_name="Invalid latitude")

    with pytest.raises(msgspec.ValidationError, match="Invalid latitude"):
        Location(latitude=-90.1, longitude=0.0, display_name="Invalid latitude")


def test_location_invalid_longitude() -> None:
    with pytest.raises(msgspec.ValidationError, match="Invalid longitude"):
        Location(latitude=0.0, longitude=180.1, display_name="Invalid longitude")

    with pytest.raises(msgspec.ValidationError, match="Invalid longitude"):
        Location(latitude=0.0, longitude=-180.1, display_name="Invalid longitude")
