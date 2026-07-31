from typing import Callable

from rich.console import RenderableType

from weather.models import Theme, WeatherResponse
from weather.ui.themes import default

THEMES = {"default": default}


def get_theme(name: Theme) -> Callable[[WeatherResponse], RenderableType]:
    module = THEMES.get(name, default)
    return getattr(module, "render_overview", default.render_overview)


def list_themes() -> list[str]:
    return list(THEMES.keys())
