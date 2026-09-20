from typing import cast

import msgspec
import pytest
from rich.columns import Columns
from rich.table import Table

import tests.constants as c
from weather.models import Theme, UnitSystem, WeatherData, WeatherResponse
from weather.ui.themes import default, get_theme, list_themes


def test_list_themes() -> None:
    assert list_themes() == ["default"]


def test_get_theme() -> None:
    renderer = get_theme(Theme.DEFAULT)
    assert renderer.render_overview is default.render_overview
    assert renderer.render_forecast is default.render_forecast

    fallback = get_theme(cast(Theme, "nonexistent"))
    assert fallback.render_overview is default.render_overview
    assert fallback.render_forecast is default.render_forecast


def test_default_render_overview_with_aqi() -> None:
    response = WeatherResponse(
        location=c.LOCATION, weather=c.WEATHER_DATA, aqi=c.AIR_QUALITY
    )
    group = default.render_overview(response)
    layout = group.renderables[1]

    assert isinstance(layout, Table)
    assert len(layout.columns) == 3

    aqi_table = layout.columns[2]._cells[0]
    assert isinstance(aqi_table, Table)
    assert aqi_table.columns[0]._cells == ["AQI", "PM2.5", "PM10", "UVI"]


@pytest.mark.parametrize("uv_index", [None, 0.0])
def test_default_render_overview_without_uvi(uv_index: float | None) -> None:
    response = WeatherResponse(
        location=c.LOCATION,
        weather=c.WEATHER_DATA,
        aqi=msgspec.structs.replace(c.AIR_QUALITY, uv_index=uv_index),
    )
    group = default.render_overview(response)
    layout = group.renderables[1]

    assert isinstance(layout, Table)
    assert len(layout.columns) == 3

    aqi_table = layout.columns[2]._cells[0]
    assert isinstance(aqi_table, Table)
    assert aqi_table.columns[0]._cells == ["AQI", "PM2.5", "PM10"]


def test_default_render_overview_without_aqi() -> None:
    response = WeatherResponse(location=c.LOCATION, weather=c.WEATHER_DATA, aqi=None)
    group = default.render_overview(response)
    layout = group.renderables[1]

    assert isinstance(layout, Table)
    assert len(layout.columns) == 2


def test_default_render_forecast() -> None:
    daily = [c.DAILY_FORECAST, c.DAILY_FORECAST]
    weather_obj = WeatherData(
        current=c.CURRENT_WEATHER,
        daily=daily,
        unit_system=UnitSystem.METRIC,
        valid_until=c.AIR_QUALITY.valid_until,
    )
    response = WeatherResponse(
        location=c.LOCATION, weather=weather_obj, aqi=c.AIR_QUALITY
    )
    columns = default.render_forecast(response, days=2)
    assert isinstance(columns, Columns)
    panels = list(columns.renderables)
    assert len(panels) == 1
