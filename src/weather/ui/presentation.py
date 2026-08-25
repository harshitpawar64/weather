from datetime import UTC, datetime

from weather.models import UnitSystem


def format_temperature(temp: float | None, units: UnitSystem) -> str:
    if temp is None:
        return "[dim]-[/]"

    celsius = temp if units is UnitSystem.METRIC else (temp - 32) * 5 / 9

    if celsius <= 0:
        color = "cyan"
    elif celsius <= 10:
        color = "bright_blue"
    elif celsius <= 20:
        color = "green"
    elif celsius <= 30:
        color = "yellow"
    elif celsius <= 40:
        color = "dark_orange"
    else:
        color = "red"

    return f"[{color}]{temp:.0f}[/]"


def aqi_category(aqi: float) -> str:
    aqi = round(aqi)
    if aqi <= 50:
        return f"[green]{aqi} [Good][/]"
    if aqi <= 100:
        return f"[yellow]{aqi} [Moderate][/]"
    if aqi <= 150:
        return f"[dark_orange]{aqi} [Unhealthy for sensitive groups][/]"
    if aqi <= 200:
        return f"[red]{aqi} [Unhealthy][/]"
    if aqi <= 300:
        return f"[magenta]{aqi} [Very unhealthy][/]"

    return f"[bright_white on dark_red]{aqi} [Hazardous][/]"


def uvi_category(uvi: float) -> str:
    if uvi <= 2:
        return f"[green]{uvi} [Low][/]"
    if uvi <= 5:
        return f"[yellow]{uvi} [Moderate][/]"
    if uvi <= 7:
        return f"[dark_orange]{uvi} [High][/]"
    if uvi <= 10:
        return f"[red]{uvi} [Very high][/]"

    return f"[magenta]{uvi} [Extreme][/]"


def wind_direction(degrees: int) -> str:
    directions = ("↑", "↗", "→", "↘", "↓", "↙", "←", "↖")
    arrow = directions[round(degrees / 45) % len(directions)]

    return f"[bold blue]{arrow}[/]"


def format_precipitation(prob: int | None) -> str:
    if prob is None:
        return "[dim]-[/]"
    if prob >= 66:
        return f"[bold cyan]{prob}% ☂[/]"
    if prob >= 33:
        return f"[cyan]{prob}%[/]"

    return f"{prob}%"


def format_wind_speed(speed: float | None, units: UnitSystem) -> str:
    if speed is None:
        return "[dim]-[/]"

    threshold = 40 if units is UnitSystem.METRIC else 25
    if speed >= threshold:
        return f"[bold yellow]{speed:.0f} {units.wind_speed} ⚠[/]"

    return f"{speed:.0f} {units.wind_speed}"


def format_updated(value: str) -> str:
    try:
        dt = datetime.fromisoformat(value)

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)

        now = datetime.now(UTC)

        diff_minutes = int((now - dt).total_seconds() / 60)

        if diff_minutes < 1:
            return "[dim]Updated just now[/]"
        if diff_minutes < 60:
            return f"[dim]Updated {diff_minutes}m ago[/]"
        if diff_minutes < 1440:
            return f"[dim]Updated {diff_minutes // 60}h ago[/]"

        return f"[dim]Updated {diff_minutes // 1440}d ago[/]"
    except (ValueError, TypeError):
        return value


def format_day(value: str) -> str:
    try:
        return datetime.fromisoformat(value).strftime("%a %d %b")
    except ValueError:
        return value


def format_sun(sunrise: str, sunset: str) -> str:
    sr = datetime.fromisoformat(sunrise)
    ss = datetime.fromisoformat(sunset)

    diff = ss - sr

    if sr.hour == ss.hour and sr.minute == ss.minute:
        return (
            "[yellow]☀ Midnight sun[/]" if diff.days == 1 else "[cyan]⏾ Polar night[/]"
        )

    return f"{sr.strftime('%H:%M')} - {ss.strftime('%H:%M')}"
