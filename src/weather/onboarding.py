from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

from weather.exceptions import ServiceError
from weather.models import Location, UnitSystem
from weather.services import GeocodingService, GeolocationService

console = Console()


async def onboarding(
    geolocator: GeolocationService, geocoder: GeocodingService
) -> tuple[Location, UnitSystem]:
    console.print(
        Panel.fit(
            "[bold cyan]Welcome to weather ⛅[/]\n"
            "[dim]Let's set up your default location and unit preferences.[/]",
            border_style="cyan",
        )
    )
    console.print()

    location = await _choose_location(geolocator, geocoder)
    unit_system = _choose_unit_system()

    console.print()
    console.print(f"[bold green]✓ Location:[/] [white]{location.display_name}[/]")
    console.print(
        f"[bold green]✓ Units:[/]    [white]{unit_system.capitalize()} "
        f"({unit_system.temperature}, {unit_system.wind_speed}, {unit_system.precipitation})[/]"
    )
    console.print("[bold green]✓ Setup complete![/]\n")

    return location, unit_system


async def _choose_location(
    geolocator: GeolocationService, geocoder: GeocodingService
) -> Location:
    try:
        with console.status("[cyan]Detecting your location...[/]", spinner="dots"):
            suggested = await geolocator.geolocate()
    except ServiceError:
        console.print(
            "[yellow]Could not automatically detect your location. Let's enter one manually.[/]"
        )
    else:
        if Confirm.ask(
            f"Use suggested location [bold white]{suggested.display_name}[/]?",
            default=True,
        ):
            return suggested

    while True:
        query = Prompt.ask("Enter a city, address, or place name").strip()
        if not query:
            console.print("[yellow]Please enter a valid location.[/]")
            continue

        try:
            with console.status(f"[cyan]Searching for '{query}'...[/]", spinner="dots"):
                return await geocoder.geocode(query)
        except ServiceError:
            console.print("[yellow]Could not find that location. Please try again.[/]")


def _choose_unit_system() -> UnitSystem:
    console.print()
    console.print("[dim]Select your preferred unit system:[/]")
    console.print(
        f"  • [cyan]metric[/]:   {UnitSystem.METRIC.temperature}, {UnitSystem.METRIC.wind_speed}, {UnitSystem.METRIC.precipitation}"
    )
    console.print(
        f"  • [cyan]imperial[/]: {UnitSystem.IMPERIAL.temperature}, {UnitSystem.IMPERIAL.wind_speed}, {UnitSystem.IMPERIAL.precipitation}"
    )
    console.print()

    value = Prompt.ask(
        "Unit system", choices=list(UnitSystem), default=UnitSystem.METRIC
    )
    return UnitSystem(value)
