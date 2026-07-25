from dataclasses import dataclass


@dataclass(frozen=True)
class WeatherCondition:
    label: str
    icon: str


_WEATHER_CONDITIONS = {
    -1: WeatherCondition(
        label="Unknown",
        icon=(
            "    .--.        \n"
            "      __)      \n"
            "    (          \n"
            "     `-᾿        \n"
            "      •         "
        ),
    ),
    0: WeatherCondition(
        label="Clear sky",
        icon=(
            "[yellow]     \\    /      [/yellow]\n"
            "[yellow]      .--.       [/yellow]\n"
            "[yellow]  __ (    ) __    [/yellow]\n"
            "[yellow]      `--`      [/yellow]\n"
            "[yellow]     /    \\      [/yellow]"
        ),
    ),
    1: WeatherCondition(
        label="Mainly clear",
        icon=(
            "[yellow]    \\__/     [/yellow]    \n"
            "[yellow]  __/  )[/yellow][grey70].--.     [/grey70]\n"
            "[yellow]    \\_[/yellow][grey70](     ).   [/grey70]\n"
            "[yellow]    /[/yellow][grey70](___(___) [/grey70]\n"
            "                 "
        ),
    ),
    2: WeatherCondition(
        label="Partly cloudy",
        icon=(
            "[yellow]    \\__/     [/yellow]    \n"
            "[yellow]  __/  [/yellow][grey70]).--.     [/grey70]\n"
            "[yellow]    \\_[/yellow][grey70](     ).   [/grey70]\n"
            "[yellow]    /[/yellow][grey70](___(___) [/grey70]\n"
            "                 "
        ),
    ),
    3: WeatherCondition(
        label="Overcast",
        icon=(
            "                 \n"
            "[grey62]    .--.     [/grey62]\n"
            "[grey62]  _(    )..   [/grey62]\n"
            "[grey62] (___.__)__) [/grey62]\n"
            "                 "
        ),
    ),
    45: WeatherCondition(
        label="Fog",
        icon=(
            "                 \n"
            "[grey74] _ - _ - _ - [/grey74]\n"
            "[grey74]  _ - _ - _  [/grey74]\n"
            "[grey74] _ - _ - _ - [/grey74]\n"
            "                 "
        ),
    ),
    48: WeatherCondition(
        label="Rime fog",
        icon=(
            "                 \n"
            "[grey74] _ - _ [white]*[/white] _ - [/grey74]\n"
            "[grey74]  _ [white]*[/white] _ - _ [white]*[/white] [/grey74]\n"
            "[grey74] _ - _ [white]*[/white] _ - [/grey74]\n"
            "                 "
        ),
    ),
    51: WeatherCondition(
        label="Light drizzle",
        icon=(
            "[grey70]    .--.       [/grey70]\n"
            "[grey70]   (    ).    [/grey70]\n"
            "[grey70]  (___(__)    [/grey70]\n"
            "[cornflower_blue]   ʻ  ʻ  ʻ   [/cornflower_blue]\n"
            "[cornflower_blue] ʻ  ʻ  ʻ    [/cornflower_blue]"
        ),
    ),
    53: WeatherCondition(
        label="Drizzle",
        icon=(
            "[grey70]    .--.       [/grey70]\n"
            "[grey70]   (    ).    [/grey70]\n"
            "[grey70]  (___(__)    [/grey70]\n"
            "[cornflower_blue]   ʻ ʻ ʻ ʻ   [/cornflower_blue]\n"
            "[cornflower_blue] ʻ ʻ ʻ ʻ    [/cornflower_blue]"
        ),
    ),
    55: WeatherCondition(
        label="Heavy drizzle",
        icon=(
            "[grey62]    .--.       [/grey62]\n"
            "[grey62]   (    ).    [/grey62]\n"
            "[grey62]  (___(__)    [/grey62]\n"
            "[dodger_blue1]  ‚ʻ‚ʻ‚ʻ‚ʻ     [/dodger_blue1]\n"
            "[dodger_blue1]  ‚ʻ‚ʻ‚ʻ‚ʻ     [/dodger_blue1]"
        ),
    ),
    56: WeatherCondition(
        label="Freezing drizzle",
        icon=(
            "[grey70]    .--.       [/grey70]\n"
            "[grey70]   (    ).    [/grey70]\n"
            "[grey70]  (___(__)    [/grey70]\n"
            "[cornflower_blue]   ʻ [white]*[/white] ʻ [white]*[/white]   \n"
            "[cornflower_blue]  [white]*[/white] ʻ [white]*[/white] ʻ     [/cornflower_blue]"
        ),
    ),
    57: WeatherCondition(
        label="Heavy freezing drizzle",
        icon=(
            "[grey62]    .--.       [/grey62]\n"
            "[grey62]   (    ).    [/grey62]\n"
            "[grey62]  (___(___)    [/grey62]\n"
            "[cornflower_blue]  ‚ʻ [white]*[/white] ‚ʻ [white]*[/white]  \n"
            "[cornflower_blue] [white]*[/white] ‚ʻ [white]*[/white] ‚ʻ    [/cornflower_blue]"
        ),
    ),
    61: WeatherCondition(
        label="Light rain",
        icon=(
            "[grey70]    .--.       [/grey70]\n"
            "[grey70]   (    ).    [/grey70]\n"
            "[grey70]  (___(__)    [/grey70]\n"
            "[cornflower_blue]   ʻ ʻ ʻ ʻ   [/cornflower_blue]\n"
            "[cornflower_blue] ʻ ʻ ʻ ʻ    [/cornflower_blue]"
        ),
    ),
    63: WeatherCondition(
        label="Rain",
        icon=(
            "[grey70]    .--.       [/grey70]\n"
            "[grey70]   (    ).    [/grey70]\n"
            "[grey70]  (___(__)    [/grey70]\n"
            "[cornflower_blue]  ‚ʻ‚ʻ‚ʻ‚ʻ     [/cornflower_blue]\n"
            "[cornflower_blue]  ‚ʻ‚ʻ‚ʻ‚ʻ     [/cornflower_blue]"
        ),
    ),
    65: WeatherCondition(
        label="Heavy rain",
        icon=(
            "[grey62]    .--.       [/grey62]\n"
            "[grey62]   (    ).    [/grey62]\n"
            "[grey62]  (___(___)    [/grey62]\n"
            "[dodger_blue1]  ‚ʻ‚ʻ‚ʻ‚ʻ‚     [/dodger_blue1]\n"
            "[dodger_blue1]  ‚ʻ‚ʻ‚ʻ‚ʻ‚     [/dodger_blue1]"
        ),
    ),
    66: WeatherCondition(
        label="Freezing rain",
        icon=(
            "[grey70]    .--.       [/grey70]\n"
            "[grey70]   (    ).    [/grey70]\n"
            "[grey70]  (___(__)    [/grey70]\n"
            "[cornflower_blue]   ʻ [white]*[/white] ʻ [white]*[/white]   \n"
            "[cornflower_blue]  [white]*[/white] ʻ [white]*[/white] ʻ     [/cornflower_blue]"
        ),
    ),
    67: WeatherCondition(
        label="Heavy freezing rain",
        icon=(
            "[grey62]    .--.       [/grey62]\n"
            "[grey62]   (    ).    [/grey62]\n"
            "[grey62]  (___(___)    [/grey62]\n"
            "[dodger_blue1]  ‚ʻ [white]*[/white] ‚ʻ [white]*[/white]  [/dodger_blue1]\n"
            "[dodger_blue1] [white]*[/white] ‚ʻ [white]*[/white] ‚ʻ    [/dodger_blue1]"
        ),
    ),
    71: WeatherCondition(
        label="Light snow",
        icon=(
            "[grey70]    .--.       [/grey70]\n"
            "[grey70]   (    ).    [/grey70]\n"
            "[grey70]  (___(__)    [/grey70]\n"
            "[white]   *    *   [/white]\n"
            "[white]  *    *    [/white]"
        ),
    ),
    73: WeatherCondition(
        label="Snow",
        icon=(
            "[grey70]    .--.       [/grey70]\n"
            "[grey70]   (    ).    [/grey70]\n"
            "[grey70]  (___(__)    [/grey70]\n"
            "[white]   *  *  *   [/white]\n"
            "[white]  *  *  *    [/white]"
        ),
    ),
    75: WeatherCondition(
        label="Heavy snow",
        icon=(
            "[grey62]    .--.       [/grey62]\n"
            "[grey62]   (    ).    [/grey62]\n"
            "[grey62]  (___(__)    [/grey62]\n"
            "[white bold]   * * * *    [/white bold]\n"
            "[white bold]  * * * *     [/white bold]"
        ),
    ),
    77: WeatherCondition(
        label="Snow grains",
        icon=(
            "[grey70]    .--.       [/grey70]\n"
            "[grey70]   (    ).    [/grey70]\n"
            "[grey70]  (___(__)    [/grey70]\n"
            "[white]   •  •  •   [/white]\n"
            "[white]  •  •  •    [/white]"
        ),
    ),
    80: WeatherCondition(
        label="Light showers",
        icon=(
            '[yellow] __/""[/yellow][grey70].--.      [/grey70]\n'
            "[yellow]   \\_[/yellow][grey70](    ).   [/grey70]\n"
            "[yellow]   /[/yellow][grey70](___(__) [/grey70]\n"
            "[cornflower_blue]     ʻ  ʻ  ʻ [/cornflower_blue]\n"
            "[cornflower_blue]  ʻ  ʻ  ʻ    [/cornflower_blue]"
        ),
    ),
    81: WeatherCondition(
        label="Showers",
        icon=(
            '[yellow] __/""[/yellow][grey70].--.      [/grey70]\n'
            "[yellow]   \\_[/yellow][grey70](    ).   [/grey70]\n"
            "[yellow]   /[/yellow][grey70](___(__) [/grey70]\n"
            "[cornflower_blue]     ʻ ʻ ʻ ʻ [/cornflower_blue]\n"
            "[cornflower_blue]  ʻ ʻ ʻ ʻ    [/cornflower_blue]"
        ),
    ),
    82: WeatherCondition(
        label="Heavy showers",
        icon=(
            '[yellow] _/""[/yellow][grey62].-.      [/grey62]\n'
            "[yellow]  ,\\_[/yellow][grey62](    ).   [/grey62]\n"
            "[yellow]   /[/yellow][grey62](___(__) [/grey62]\n"
            "[dodger_blue1]   ‚ʻ‚ʻ‚ʻ‚ʻ   [/dodger_blue1]\n"
            "[dodger_blue1]   ‚ʻ‚ʻ‚ʻ‚ʻ   [/dodger_blue1]"
        ),
    ),
    85: WeatherCondition(
        label="Light snow showers",
        icon=(
            '[yellow] __/""[/yellow][grey70].--.      [/grey70]\n'
            "[yellow]   \\_[/yellow][grey70](    ).   [/grey70]\n"
            "[yellow]   /[/yellow][grey70](___(__) [/grey70]\n"
            "[white bold]     *  *  * [/white bold]\n"
            "[white bold]  *  *  *   [/white bold]"
        ),
    ),
    86: WeatherCondition(
        label="Heavy snow showers",
        icon=(
            '[yellow] __/""[/yellow][grey62].--.      [/grey62]\n'
            "[yellow]   \\_[/yellow][grey62](    ).   [/grey62]\n"
            "[yellow]   /[/yellow][grey62](___(__) [/grey62]\n"
            "[white bold]    * * * *   [/white bold]\n"
            "[white bold]   * * * *    [/white bold]"
        ),
    ),
    95: WeatherCondition(
        label="Thunderstorm",
        icon=(
            '[yellow] __/""[/yellow][grey70].--.      [/grey70]\n'
            "[yellow]   \\_[/yellow][grey70](    ).   [/grey70]\n"
            "[yellow]   /[/yellow][grey70](___(___) [/grey70]\n"
            "[cornflower_blue]   ʻ ʻ [yellow blink]⚡[/yellow blink] ʻ ʻ [/cornflower_blue]\n"
            "[cornflower_blue]  ʻ [yellow blink]⚡[/yellow blink] ʻ ʻ ʻ    [/cornflower_blue]"
        ),
    ),
    96: WeatherCondition(
        label="Thunderstorm with hail",
        icon=(
            '[yellow] __/""[/yellow][grey70].--.      [/grey70]\n'
            "[yellow]   \\_[/yellow][grey70](    ).   [/grey70]\n"
            "[yellow]   /[/yellow][grey70](___(___) [/grey70]\n"
            "[cornflower_blue]   ʻ [white]•[/white] [yellow blink]⚡[/yellow blink] ʻ [white]•[/white] [/cornflower_blue]\n"
            "[cornflower_blue]  [white]•[/white] [yellow blink]⚡[/yellow blink] ʻ [white]•[/white] ʻ    [/cornflower_blue]"
        ),
    ),
    99: WeatherCondition(
        label="Severe thunderstorm with hail",
        icon=(
            '[yellow] __/""[/yellow][grey62].--.      [/grey62]\n'
            "[yellow]   \\_[/yellow][grey62](    )..   [/grey62]\n"
            "[yellow]   /[/yellow][grey62](___(____) [/grey62]\n"
            "[dodger_blue1]   ʻ [white]•[/white] [yellow blink]⚡[/yellow blink] ʻ [white]•[/white] ʻ [/dodger_blue1]\n"
            "[dodger_blue1]  [white]•[/white] [yellow blink]⚡[/yellow blink] [white]•[/white] [yellow blink]⚡[/yellow blink] ʻ [white]•[/white] [/dodger_blue1]"
        ),
    ),
}


def weather_condition(wmo_code: int) -> WeatherCondition:
    return _WEATHER_CONDITIONS.get(wmo_code, _WEATHER_CONDITIONS[-1])


if __name__ == "__main__":
    from rich.console import Console
    from rich.text import Text

    console = Console()

    for code, condition in _WEATHER_CONDITIONS.items():
        t = Text()
        t.append(f"WMO Code: {code} | Label: {condition.label}\n", style="bold yellow")
        t.append(Text.from_markup(condition.icon))
        t.append("\n" + "-" * 30 + "\n")
        console.print(t)
