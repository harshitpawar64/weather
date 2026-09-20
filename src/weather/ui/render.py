from rich.console import Console

from weather.models import Theme, WeatherResponse
from weather.ui.themes import get_theme

console = Console()


def render_weather(
    response: WeatherResponse, theme: Theme = Theme.DEFAULT, days: int = 7
) -> None:
    renderer = get_theme(theme)

    console.print(renderer.render_overview(response))

    if days > 1:
        console.print("")
        console.print(renderer.render_forecast(response, days))
