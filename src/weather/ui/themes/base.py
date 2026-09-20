from collections.abc import Callable
from dataclasses import dataclass

from rich.console import RenderableType

from weather.models import Theme, WeatherResponse
from weather.ui.themes import default


@dataclass(frozen=True)
class ThemeRenderer:
    render_overview: Callable[[WeatherResponse], RenderableType]
    render_forecast: Callable[[WeatherResponse, int], RenderableType]


THEMES = {"default": default}


def get_theme(name: Theme) -> ThemeRenderer:
    module = THEMES.get(name, default)
    return ThemeRenderer(
        render_overview=getattr(module, "render_overview", default.render_overview),
        render_forecast=getattr(module, "render_forecast", default.render_forecast),
    )


def list_themes() -> list[str]:
    return list(THEMES.keys())
