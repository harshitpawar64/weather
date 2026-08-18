from rich.align import Align
from rich.console import Group
from rich.table import Table

from weather.models import AirQuality, WeatherResponse
from weather.ui.conditions import weather_condition
from weather.ui.presentation import (
    aqi_category,
    format_precipitation,
    format_temperature,
    format_updated,
    wind_direction,
)


def render_overview(response: WeatherResponse) -> Group:
    weather = response.weather
    current = weather.current
    today = weather.daily[0]
    units = weather.unit_system
    aqi = response.aqi

    actual_temp = format_temperature(current.temperature, units)
    feels_like = format_temperature(current.apparent_temperature, units)

    condition = weather_condition(current.weather_code, is_day=current.is_day)

    current_table = Table.grid(padding=(0, 3))
    current_table.add_column(style="dim")
    current_table.add_column(style="white")

    current_table.add_row("Condition", condition.label)

    current_table.add_row(
        "Temp", f"{actual_temp}([bold]{feels_like}[/]) {units.temperature}"
    )
    current_table.add_row("Humidity", f"{current.humidity}%")
    current_table.add_row(
        "Wind",
        f"{wind_direction(current.wind_direction)} {current.wind_speed:.0f}([bold]{current.wind_gusts:.0f}[/]) {units.wind_speed}",
    )
    current_table.add_row(
        "Precip",
        f"{current.precipitation:g} {units.precipitation} | {format_precipitation(today.precipitation_prob_max)}",
    )

    columns = [condition.icon, current_table]

    if aqi:
        columns.append(_render_aqi(aqi))

    layout = Table.grid(padding=(1, 4))
    layout.add_row(*columns)

    return Group(
        f"[bold green]📍 {response.location.display_name}[/]\n",
        layout,
        Align.right(format_updated(current.time)),
    )


def _render_aqi(aqi: AirQuality) -> Table:
    table = Table.grid(padding=(0, 3))
    table.add_column(style="dim")
    table.add_column(style="bold white")

    table.add_row("AQI", aqi_category(aqi.us_aqi))
    table.add_row("PM2.5", f"{aqi.pm_2_5} µg/m³")
    table.add_row("PM10", f"{aqi.pm_10} µg/m³")

    return table
