from rich.align import Align
from rich.columns import Columns
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from weather.models import WeatherResponse
from weather.ui.conditions import weather_condition
from weather.ui.presentation import (
    aqi_category,
    format_precipitation,
    format_updated,
    wind_direction,
)

console = Console()


def render_overview(response: WeatherResponse) -> Group:
    current_columns = Columns(
        [_current_panel(response), _air_quality_panel(response)],
        expand=True,
        equal=console.width >= 70,
    )

    location = response.location
    location_text = (
        f"Location: {location.display_name} [{location.latitude}, {location.longitude}]"
    )

    return Group(current_columns, "", location_text)


def _current_panel(response: WeatherResponse) -> Panel:
    weather = response.weather
    current = weather.current
    today = weather.daily[0]
    units = weather.unit_system
    condition = weather_condition(current.weather_code, is_day=current.is_day)

    icon = Align.center(condition.icon)
    label = Align.center(Text(condition.label, style="bold cyan"))

    temp_text = Text()
    temp_text.append(
        f"{current.temperature:.0f}{units.temperature}", style="bold white"
    )
    temp_text.append(
        f"  Feels like {current.apparent_temperature:.0f}{units.temperature}",
        style="green" if current.apparent_temperature <= current.temperature else "red",
    )
    temp = Align.center(temp_text)

    details = Table.grid(expand=True, padding=(0, 2))
    details.add_column(style="dim")
    details.add_column(style="bold white")
    details.add_column(style="dim", justify="right")
    details.add_column(style="bold white", justify="right")

    details.add_row(
        "Humidity",
        f"{current.humidity}%",
        "Wind",
        f"{wind_direction(current.wind_direction)} {current.wind_speed:.0f} {units.wind_speed}",
    )
    details.add_row(
        "Precip",
        f"{current.precipitation:g} {units.precipitation} | {format_precipitation(today.precipitation_prob_max)}",
        "Gusts",
        f"{current.wind_gusts:.0f} {units.wind_speed}",
    )

    return Panel(
        Group(
            icon,
            label,
            temp,
            "",
            details,
            "",
            Align.right(format_updated(current.time)),
        ),
        border_style="cyan",
        padding=(1, 2),
    )


def _air_quality_panel(response: WeatherResponse) -> Panel:
    aqi = response.aqi
    category = aqi_category(aqi.us_aqi)

    hero = Align.center(category)

    table = Table.grid(expand=True, padding=(0, 1))
    table.add_column(style="dim")
    table.add_column(justify="right", style="bold white")
    table.add_row("PM2.5", f"{aqi.pm_2_5:g} µg/m³")
    table.add_row("PM10", f"{aqi.pm_10:g} µg/m³")

    return Panel(
        Group(hero, "", "", table),
        title=Text("Air quality", style="bold magenta"),
        border_style="magenta",
        padding=(1, 2),
    )
