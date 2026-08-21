from typing import cast

from rich.console import Group

import tests.constants as c
from weather.models import Theme, WeatherResponse
from weather.ui.themes import get_theme, list_themes
from weather.ui.themes.default import render_overview


def test_list_themes() -> None:
    assert list_themes() == ["default"]


def test_get_theme() -> None:
    assert get_theme(Theme.DEFAULT) is render_overview
    assert get_theme(cast(Theme, "nonexistent")) is render_overview


def test_render_overview_with_aqi() -> None:
    response = WeatherResponse(
        location=c.LOCATION, weather=c.WEATHER_DATA, aqi=c.AIR_QUALITY
    )
    group = render_overview(response)
    assert isinstance(group, Group)


def test_render_overview_without_aqi() -> None:
    response = WeatherResponse(location=c.LOCATION, weather=c.WEATHER_DATA, aqi=None)
    group = render_overview(response)
    assert isinstance(group, Group)
