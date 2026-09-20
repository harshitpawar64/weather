from rich.align import Align
from rich.columns import Columns
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from weather.models import DailyForecast, UnitSystem, WeatherResponse
from weather.ui.conditions import weather_condition
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
        format_precipitation(
            today.precipitation_prob_max, today.precipitation_sum, units
        ),
    )

    columns = [condition.icon, current_table]

    if aqi:
        aqi_table = Table.grid(padding=(0, 3))
        aqi_table.add_column(style="dim")
        aqi_table.add_column(style="bold white")

        aqi_table.add_row("AQI", aqi_category(aqi.us_aqi))
        aqi_table.add_row("PM2.5", f"{aqi.pm_2_5} µg/m³")
        aqi_table.add_row("PM10", f"{aqi.pm_10} µg/m³")

        if aqi.uv_index:
            aqi_table.add_row("UVI", uvi_category(aqi.uv_index))

        columns.append(aqi_table)

    layout = Table.grid(padding=(1, 4))
    layout.add_row(*columns)

    return Group(
        f"[bold green]📍 {response.location.display_name}[/]\n",
        layout,
        Align.right(format_updated(current.time)),
    )


def render_forecast(response: WeatherResponse, days: int) -> Columns:
    weather = response.weather
    units = weather.unit_system
    panels = (_forecast_panel(day, units) for day in weather.daily[1:days])
    return Columns(panels, equal=True, padding=(0, 3))


def _forecast_panel(day: DailyForecast, units: UnitSystem) -> Panel:
    condition = weather_condition(day.weather_code)

    icon = Align.center(condition.icon)
    label = Align.center(Text(condition.label, style="bold cyan"))

    temp_min = format_temperature(day.temp_min, units)
    temp_max = format_temperature(day.temp_max, units)

    temp = Align.center(
        f"{temp_min} / {temp_max} {units.temperature}", style="bold white"
    )

    details = Table.grid(expand=True, padding=(0, 1))
    details.add_column(style="dim")
    details.add_column(justify="right", style="bold white")
    details.add_row(
        "Precip",
        format_precipitation(day.precipitation_prob_max, day.precipitation_sum, units),
    )
    details.add_row("Wind", format_wind_speed(day.wind_speed_max, units))
    details.add_row("Sun", format_sun(day.sunrise, day.sunset))

    return Panel(
        Group(icon, "", label, temp, "", details),
        title=Text(format_day(day.date), style="bold green"),
        border_style="green",
        padding=(1, 1),
    )
