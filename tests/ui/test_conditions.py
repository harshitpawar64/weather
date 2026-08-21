import pytest

from weather.ui.conditions import weather_condition


def test_weather_condition_none() -> None:
    cond = weather_condition(None)
    assert cond.label == "Unknown"
    assert cond.icon != ""


def test_weather_condition_unknown_code() -> None:
    cond = weather_condition(99999)
    assert cond.label == "Unknown"
    assert cond.icon != ""


@pytest.mark.parametrize(
    ("wmo_code", "expected_label"),
    [
        (0, "Clear sky"),
        (1, "Mainly clear"),
        (2, "Partly cloudy"),
        (3, "Overcast"),
        (45, "Fog"),
        (48, "Rime fog"),
        (51, "Light drizzle"),
        (53, "Drizzle"),
        (55, "Heavy drizzle"),
        (56, "Freezing drizzle"),
        (57, "Heavy freezing drizzle"),
        (61, "Light rain"),
        (63, "Rain"),
        (65, "Heavy rain"),
        (66, "Freezing rain"),
        (67, "Heavy freezing rain"),
        (71, "Light snow"),
        (73, "Snow"),
        (75, "Heavy snow"),
        (77, "Snow grains"),
        (80, "Light showers"),
        (81, "Showers"),
        (82, "Heavy showers"),
        (85, "Light snow showers"),
        (86, "Heavy snow showers"),
        (95, "Thunderstorm"),
        (96, "Thunderstorm with hail"),
        (99, "Severe thunderstorm with hail"),
    ],
)
def test_weather_condition_day_codes(wmo_code: int, expected_label: str) -> None:
    cond = weather_condition(wmo_code, is_day=True)
    assert cond.label == expected_label
    assert cond.icon != ""


@pytest.mark.parametrize(
    ("wmo_code", "expected_label"),
    [
        (0, "Clear night"),
        (1, "Mainly clear"),
        (2, "Partly cloudy"),
        (80, "Light showers"),
        (81, "Showers"),
        (82, "Heavy showers"),
        (85, "Light snow showers"),
        (86, "Heavy snow showers"),
        (95, "Thunderstorm"),
        (96, "Thunderstorm with hail"),
        (99, "Severe thunderstorm with hail"),
    ],
)
def test_weather_condition_night_overrides(wmo_code: int, expected_label: str) -> None:
    cond = weather_condition(wmo_code, is_day=False)
    assert cond.label == expected_label
    assert cond.icon != ""
