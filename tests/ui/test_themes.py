from typing import cast

import msgspec
import pytest
from rich.table import Table

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
    layout = group.renderables[1]

    assert isinstance(layout, Table)
    assert len(layout.columns) == 3

    aqi_table = layout.columns[2]._cells[0]
    assert isinstance(aqi_table, Table)
    assert aqi_table.columns[0]._cells == ["AQI", "PM2.5", "PM10", "UVI"]


@pytest.mark.parametrize("uv_index", [None, 0.0])
def test_render_overview_without_uvi(uv_index: float | None) -> None:
    response = WeatherResponse(
        location=c.LOCATION,
        weather=c.WEATHER_DATA,
        aqi=msgspec.structs.replace(c.AIR_QUALITY, uv_index=uv_index),
    )
    group = render_overview(response)
    layout = group.renderables[1]

    assert isinstance(layout, Table)
    assert len(layout.columns) == 3

    aqi_table = layout.columns[2]._cells[0]
    assert isinstance(aqi_table, Table)
    assert aqi_table.columns[0]._cells == ["AQI", "PM2.5", "PM10"]


def test_render_overview_without_aqi() -> None:
    response = WeatherResponse(location=c.LOCATION, weather=c.WEATHER_DATA, aqi=None)
    group = render_overview(response)
    layout = group.renderables[1]

    assert isinstance(layout, Table)
    assert len(layout.columns) == 2
