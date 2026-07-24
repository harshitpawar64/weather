from rich.console import Console
from rich.prompt import Confirm, Prompt

from weather.models import Location, UnitSystem
from weather.services import GeocodingService, GeolocationService

console = Console()


async def onboarding(
    geolocator: GeolocationService, geocoder: GeocodingService
) -> tuple[Location, UnitSystem]:
    console.print("[bold cyan]Welcome to weather[/]")

    location = await _choose_location(geolocator, geocoder)
    unit_system = _choose_unit_system()

    console.print(f"[bold green]✓ Location set to {location.display_name}[/]")
    console.print("[bold green]✓ Setup complete[/]")

    return location, unit_system


async def _choose_location(
    geolocator: GeolocationService, geocoder: GeocodingService
) -> Location:
    try:
        suggested = await geolocator.geolocate()
    except RuntimeError:
        console.print(
            "[yellow]Couldn't detect a location. Please enter one manually.[/]"
        )
    else:
        if Confirm.ask(
            f"Use suggested location [italic]{suggested.display_name}[/]?", default=True
        ):
            return suggested

    while True:
        query = Prompt.ask("Enter a location").strip()
        if not query:
            console.print("[yellow]Enter a city, address, or place name.[/]")
            continue

        try:
            return await geocoder.geocode(query)
        except RuntimeError:
            console.print("[yellow]Couldn't find that location. Try again.[/]")


def _choose_unit_system() -> UnitSystem:
    value = Prompt.ask(
        "Select unit system", choices=list(UnitSystem), default=UnitSystem.METRIC
    )
    return UnitSystem(value)
