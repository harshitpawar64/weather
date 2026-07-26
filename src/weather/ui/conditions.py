from dataclasses import dataclass

STAR = "[yellow blink]✧[/]"
BOLT = "[yellow blink]⚡[/]"
SNOW = "[white]*[/]"
HSNOW = "[bold white]*[/]"
HAIL = "[white]•[/]"
DROP = "[cornflower_blue]ʻ[/]"
RDROP = "[cornflower_blue]‚ʻ[/]"
HDROP = "[dodger_blue1]‚ʻ[/]"

# fmt:off
_UNKNOWN = (
    "    .--.\n"
    "      __)\n"
    "    (\n"
    "     `-᾿\n"
    "      •"
)

_SUN = (
    "[yellow]     \\    /[/]\n"
    "[yellow]      .--.[/]\n"
    "[yellow]  __ (    ) __[/]\n"
    "[yellow]      `--`[/]\n"
    "[yellow]     /    \\[/]"
)

_DAY_LIGHT_CLOUD = (
    "[yellow]   \\__/[/]\n"
    '[yellow] __/  )[/][grey70]--.[/]\n'
    "[yellow]   \\_[/][grey70](    ).[/]\n"
    "[yellow]   /[/][grey70](___(___)[/]\n"
)

_DAY_HEAVY_CLOUD = (
    "[yellow]   \\__/[/]\n"
    '[yellow] __/  )[/][grey62]--.[/]\n'
    "[yellow]   \\_[/][grey62](    ).[/]\n"
    "[yellow]   /[/][grey62](___(___)[/]\n"
)

_MOON = (
    f"[cyan]  {STAR} .._[/]\n"
    "[cyan]  .' .-`[/]\n"
    f"[cyan] /  /   {STAR}[/]\n"
    "[cyan] \\  \\[/]\n"
    f"[cyan]{STAR} '._`_.[/]"
)

_NIGHT_LIGHT_CLOUD = (
    "[cyan]  ,-,[/]\n"
    "[cyan] /.( [/][grey70]  .--.[/]\n"
    "[cyan] \\ {[/][grey70]  (    ).[/]\n"
    "[cyan]  `-`[/][grey70](___(___)[/]\n"
)


_NIGHT_HEAVY_CLOUD = (
    "[cyan]  ,-,[/]\n"
    "[cyan] /.( [/][grey62]  .--.[/]\n"
    "[cyan] \\ {[/][grey62]  (    ).[/]\n"
    "[cyan]  `-`[/][grey62](___(___)[/]\n"
)

_LIGHT_CLOUD = (
    "[grey70]    .--.[/]\n"
    "[grey70]   (    ).[/]\n"
    "[grey70]  (___(___)[/]\n"
)

_HEAVY_CLOUD = (
    "[grey62]    .--.[/]\n"
    "[grey62]   (    ).[/]\n"
    "[grey62]  (___(___)[/]\n"
)

_OVERCAST = (
    "\n"
    "[grey62]    .--.[/]\n"
    "[grey62]  _(    )..[/]\n"
    "[grey62] (___.__)__)[/]\n"
)

_FOG = (
    "\n"
    "[grey74] _ - _ - _ -[/]\n"
    "[grey74]  _ - _ - _ [/]\n"
    "[grey74] _ - _ - _ -[/]\n"
)

_RIME_FOG = (
    "\n"
    f"[grey74] _ - _ {SNOW} _ -[/]\n"
    f"[grey74]  _ {SNOW} _ - _ {SNOW}[/]\n"
    f"[grey74] _ - _ {SNOW} _ -[/]\n"
)

_DRIZZLE_LIGHT = (
    f"   {DROP}  {DROP}  {DROP}\n"
    f" {DROP}  {DROP}  {DROP}"
)

_DRIZZLE = (
    f"   {DROP} {DROP} {DROP} {DROP}\n"
    f" {DROP} {DROP} {DROP} {DROP}"
)

_DRIZZLE_HEAVY = (
    f"  {HDROP}{HDROP}{HDROP}{HDROP}\n"
    f"  {HDROP}{HDROP}{HDROP}{HDROP}"
)

_RAIN = (
    f"  {RDROP}{RDROP}{RDROP}{RDROP}\n"
    f"  {RDROP}{RDROP}{RDROP}{RDROP}"
)

_RAIN_HEAVY = (
    f" {HDROP}{HDROP}{HDROP}{HDROP}{HDROP}\n"
    f"{HDROP}{HDROP}{HDROP}{HDROP}{HDROP}"
)

_FREEZING_LIGHT = (
    f"   {DROP} {SNOW} {DROP} {SNOW}\n"
    f"  {SNOW} {DROP} {SNOW} {DROP}"
)

_FREEZING_HEAVY = (
    f"  {RDROP} {SNOW} {RDROP} {SNOW}\n"
    f" {SNOW} {RDROP} {SNOW} {RDROP}"
)

_FREEZING_RAIN_HEAVY = (
    f"  {HDROP} {SNOW} {HDROP} {SNOW}\n"
    f" {SNOW} {HDROP} {SNOW} {HDROP}"
)

_SNOW_LIGHT = (
    f"   {SNOW}   {SNOW}\n"
    f"  {SNOW}   {SNOW}"
)

_SNOW = (
    f"   {SNOW}  {SNOW}  {SNOW}\n"
    f"  {SNOW}  {SNOW}  {SNOW}"
)

_SNOW_HEAVY = (
    f"   {HSNOW} {HSNOW} {HSNOW} {HSNOW}\n"
    f"  {HSNOW} {HSNOW} {HSNOW} {HSNOW}"
)

_SNOW_GRAINS = (
    f"   {HAIL}  {HAIL}  {HAIL}\n"
    f"  {HAIL}  {HAIL}  {HAIL}"
)

_SHOWERS_LIGHT = (
    f"     {DROP}  {DROP}  {DROP}\n"
    f"    {DROP}  {DROP}  {DROP}"
)

_SHOWERS = (
    f"     {DROP} {DROP} {DROP} {DROP}\n"
    f"    {DROP} {DROP} {DROP} {DROP}"
)

_SHOWERS_HEAVY = (
    f"    {HDROP}{HDROP}{HDROP}{HDROP}\n"
    f"   {HDROP}{HDROP}{HDROP}{HDROP}"
)

_SNOW_SHOWERS_LIGHT = (
    f"     {HSNOW}  {HSNOW}  {HSNOW}\n"
    f"    {HSNOW}  {HSNOW}  {HSNOW}"
)

_SNOW_SHOWERS_HEAVY = (
    f"    {HSNOW} {HSNOW} {HSNOW} {HSNOW}\n"
    f"   {HSNOW} {HSNOW} {HSNOW} {HSNOW}"
)

_STORM = (
    f"    {DROP} {DROP} {BOLT} {DROP}\n"
    f"   {DROP} {BOLT} {DROP} {DROP}"
)

_STORM_HAIL = (
    f"    {HAIL} {DROP} {BOLT} {HAIL}\n"
    f"   {DROP} {BOLT} {HAIL} {DROP}"
)

_STORM_SEVERE = (
    f"   {HDROP} {HAIL} {BOLT}{HDROP} {HAIL}\n"
    f"  {HAIL} {BOLT} {HAIL} {BOLT}{HDROP}"
)

# fmt: on
@dataclass(frozen=True)
class WeatherCondition:
    label: str
    icon: str


_WEATHER_CONDITIONS = {
    -1: WeatherCondition(label="Unknown", icon=_UNKNOWN),
    0: WeatherCondition(label="Clear sky", icon=_SUN),
    1: WeatherCondition(label="Mainly clear", icon=_DAY_LIGHT_CLOUD),
    2: WeatherCondition(label="Partly cloudy", icon=_DAY_LIGHT_CLOUD),
    3: WeatherCondition(label="Overcast", icon=_OVERCAST),
    45: WeatherCondition(label="Fog", icon=_FOG),
    48: WeatherCondition(label="Rime fog", icon=_RIME_FOG),
    51: WeatherCondition(label="Light drizzle", icon=_LIGHT_CLOUD + _DRIZZLE_LIGHT),
    53: WeatherCondition(label="Drizzle", icon=_LIGHT_CLOUD + _DRIZZLE),
    55: WeatherCondition(label="Heavy drizzle", icon=_HEAVY_CLOUD + _DRIZZLE_HEAVY),
    56: WeatherCondition(label="Freezing drizzle", icon=_LIGHT_CLOUD + _FREEZING_LIGHT),
    57: WeatherCondition(
        label="Heavy freezing drizzle", icon=_HEAVY_CLOUD + _FREEZING_HEAVY
    ),
    61: WeatherCondition(label="Light rain", icon=_LIGHT_CLOUD + _DRIZZLE),
    63: WeatherCondition(label="Rain", icon=_LIGHT_CLOUD + _RAIN),
    65: WeatherCondition(label="Heavy rain", icon=_HEAVY_CLOUD + _RAIN_HEAVY),
    66: WeatherCondition(label="Freezing rain", icon=_LIGHT_CLOUD + _FREEZING_LIGHT),
    67: WeatherCondition(
        label="Heavy freezing rain", icon=_HEAVY_CLOUD + _FREEZING_RAIN_HEAVY
    ),
    71: WeatherCondition(label="Light snow", icon=_LIGHT_CLOUD + _SNOW_LIGHT),
    73: WeatherCondition(label="Snow", icon=_LIGHT_CLOUD + _SNOW),
    75: WeatherCondition(label="Heavy snow", icon=_HEAVY_CLOUD + _SNOW_HEAVY),
    77: WeatherCondition(label="Snow grains", icon=_LIGHT_CLOUD + _SNOW_GRAINS),
    80: WeatherCondition(label="Light showers", icon=_DAY_LIGHT_CLOUD + _SHOWERS_LIGHT),
    81: WeatherCondition(label="Showers", icon=_DAY_LIGHT_CLOUD + _SHOWERS),
    82: WeatherCondition(label="Heavy showers", icon=_DAY_HEAVY_CLOUD + _SHOWERS_HEAVY),
    85: WeatherCondition(
        label="Light snow showers", icon=_DAY_LIGHT_CLOUD + _SNOW_SHOWERS_LIGHT
    ),
    86: WeatherCondition(
        label="Heavy snow showers", icon=_DAY_HEAVY_CLOUD + _SNOW_SHOWERS_HEAVY
    ),
    95: WeatherCondition(label="Thunderstorm", icon=_DAY_LIGHT_CLOUD + _STORM),
    96: WeatherCondition(
        label="Thunderstorm with hail", icon=_DAY_LIGHT_CLOUD + _STORM_HAIL
    ),
    99: WeatherCondition(
        label="Severe thunderstorm with hail", icon=_DAY_HEAVY_CLOUD + _STORM_SEVERE
    ),
}

_NIGHT_OVERRIDES = {
    0: WeatherCondition(label="Clear night", icon=_MOON),
    1: WeatherCondition(label="Mainly clear", icon=_NIGHT_LIGHT_CLOUD),
    2: WeatherCondition(label="Partly cloudy", icon=_NIGHT_LIGHT_CLOUD),
    80: WeatherCondition(
        label="Light showers", icon=_NIGHT_LIGHT_CLOUD + _SHOWERS_LIGHT
    ),
    81: WeatherCondition(label="Showers", icon=_NIGHT_LIGHT_CLOUD + _SHOWERS),
    82: WeatherCondition(
        label="Heavy showers", icon=_NIGHT_HEAVY_CLOUD + _SHOWERS_HEAVY
    ),
    85: WeatherCondition(
        label="Light snow showers", icon=_NIGHT_LIGHT_CLOUD + _SNOW_SHOWERS_LIGHT
    ),
    86: WeatherCondition(
        label="Heavy snow showers", icon=_NIGHT_HEAVY_CLOUD + _SNOW_SHOWERS_HEAVY
    ),
    95: WeatherCondition(label="Thunderstorm", icon=_NIGHT_LIGHT_CLOUD + _STORM),
    96: WeatherCondition(
        label="Thunderstorm with hail", icon=_NIGHT_LIGHT_CLOUD + _STORM_HAIL
    ),
    99: WeatherCondition(
        label="Severe thunderstorm with hail", icon=_NIGHT_HEAVY_CLOUD + _STORM_SEVERE
    ),
}


def weather_condition(wmo_code: int, is_day: bool = True) -> WeatherCondition:
    if not is_day and wmo_code in _NIGHT_OVERRIDES:
        return _NIGHT_OVERRIDES[wmo_code]

    return _WEATHER_CONDITIONS.get(wmo_code, _WEATHER_CONDITIONS[-1])
