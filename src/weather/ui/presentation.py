from datetime import datetime, timezone


def format_temperature(temp: float, unit: str):
    celsius = temp if "C" in unit else (temp - 32) * 5 / 9

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


def wind_direction(degrees: int) -> str:
    directions = ("↑", "↗", "→", "↘", "↓", "↙", "←", "↖")
    arrow = directions[round(degrees / 45) % len(directions)]
    return f"[bold blue]{arrow}[/]"


def format_precipitation(prob: int) -> str:
    if prob >= 70:
        return f"[bold cyan]{prob}% ☂[/]"
    if prob >= 33:
        return f"[cyan]{prob}%[/]"
    return f"[dim]{prob}%[/]"


def format_wind_speed(speed: float, unit: str) -> str:
    threshold = 40 if "km" in unit else 25
    if speed >= threshold:
        return f"[bold yellow]{speed:.0f} {unit} ⚠[/]"
    return f"{speed:.0f} {unit}"


def format_updated(value: str) -> str:
    try:
        dt = datetime.fromisoformat(value)

        if dt.tzinfo:
            now = datetime.now(timezone.utc)
        else:
            now = datetime.now()

        diff_minutes = int((now - dt).total_seconds() / 60)

        if diff_minutes < 1:
            return "[dim]Updated just now[/]"
        if diff_minutes < 60:
            return f"[dim]Updated {diff_minutes}m ago[/]"
        if diff_minutes < 1440:
            return f"[dim]Updated {diff_minutes // 60}h ago[/]"

        return f"[dim]Updated {diff_minutes // 1440}d ago[/]"
    except ValueError, TypeError:
        return value


def format_day(value: str) -> str:
    try:
        return datetime.fromisoformat(value).strftime("%a %d %b")
    except ValueError:
        return value


def format_clock(value: str) -> str:
    try:
        return datetime.fromisoformat(value).strftime("%H:%M")
    except ValueError:
        return value
