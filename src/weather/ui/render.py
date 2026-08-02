from rich.align import Align
from rich.columns import Columns
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from weather.models import DailyForecast, Theme, UnitSystem, WeatherResponse
from weather.ui.conditions import weather_condition
from weather.ui.presentation import (
    format_clock,
    format_day,
    format_precipitation,
    format_temperature,
    format_wind_speed,
)
from weather.ui.themes import get_theme

console = Console()


def render_weather(
    response: WeatherResponse, theme: Theme = Theme.DEFAULT, days: int = 7
) -> None:
    overview = get_theme(theme)

    console.print(overview(response))

    if days > 1:
        console.print("")
        console.print(_forecast_panels(response, days))


def _forecast_panels(response: WeatherResponse, days: int) -> Columns:
    weather = response.weather
    units = weather.unit_system
    panels = (_forecast_panel(day, units) for day in weather.daily[1:days])
    return Columns(panels, equal=True, expand=True)


def _forecast_panel(day: DailyForecast, units: UnitSystem) -> Panel:
    condition = weather_condition(day.weather_code)

    icon = Align.center(condition.icon)
    label = Align.center(Text(condition.label, style="bold cyan"))

    temp_min = format_temperature(day.temp_min, units.temperature)
    temp_max = format_temperature(day.temp_max, units.temperature)

    temp = Align.center(
        f"{temp_min} / {temp_max} {units.temperature}", style="bold white"
    )

    details = Table.grid(expand=True, padding=(0, 1))
    details.add_column(style="dim")
    details.add_column(justify="right", style="bold white")
    details.add_row("Precip", format_precipitation(day.precipitation_prob_max))
    details.add_row("Wind", format_wind_speed(day.wind_speed_max, units.wind_speed))
    details.add_row("Sun", f"{format_clock(day.sunrise)} - {format_clock(day.sunset)}")

    return Panel(
        Group(icon, "", label, temp, "", details),
        title=Text(format_day(day.date), style="bold green"),
        border_style="green",
        padding=(1, 1),
    )
