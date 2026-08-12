import pytest

import tests.constants as c
from weather.models import Location, UnitSystem


def test_unit_system_properties() -> None:
    assert UnitSystem.METRIC.temperature == "°C"
    assert UnitSystem.METRIC.wind_speed == "km/h"
    assert UnitSystem.METRIC.precipitation == "mm"

    assert UnitSystem.IMPERIAL.temperature == "°F"
    assert UnitSystem.IMPERIAL.wind_speed == "mph"
    assert UnitSystem.IMPERIAL.precipitation == "in"


def test_location_valid() -> None:
    location = c.LOCATION
    assert location.latitude == c.LATITUDE
    assert location.longitude == c.LONGITUDE
    assert location.display_name == c.DISPLAY_NAME


def test_location_invalid_latitude() -> None:
    with pytest.raises(ValueError, match="Invalid latitude"):
        Location(latitude=91.0, longitude=0.0, display_name="Invalid latitude")

    with pytest.raises(ValueError, match="Invalid latitude"):
        Location(latitude=-90.1, longitude=0.0, display_name="Invalid latitude")


def test_location_invalid_longitude() -> None:
    with pytest.raises(ValueError, match="Invalid longitude"):
        Location(latitude=0.0, longitude=180.1, display_name="Invalid longitude")

    with pytest.raises(ValueError, match="Invalid longitude"):
        Location(latitude=0.0, longitude=-180.1, display_name="Invalid longitude")
