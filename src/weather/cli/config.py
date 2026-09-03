import asyncio
from typing import Annotated

import httpx
import typer
from rich.console import Console
from rich.table import Table

from weather.cache import Cache
from weather.config import Config
from weather.exceptions import ServiceError
from weather.models import Location, Theme, UnitSystem
from weather.services import GeocodingService

app = typer.Typer(name="config", help="Manage configuration")

console = Console()
err_console = Console(stderr=True)


@app.command()
def path() -> None:
    print(Config().file.resolve())


@app.command()
def show() -> None:
    config = Config()
    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold cyan")
    table.add_column(style="white")

    location = (
        f"{loc.display_name} [dim]({loc.latitude:.4f}, {loc.longitude:.4f})[/]"
        if (loc := config.location)
        else "[dim]Not set[/]"
    )

    table.add_row("Location:", location)
    table.add_row("Units:", config.unit_system.label)
    table.add_row("Theme:", config.theme)

    console.print(table)


@app.command(name="set")
def set_(
    location: Annotated[
        str | None,
        typer.Option(
            "--location", "-l", help="Default city, landmark, address or postal code."
        ),
    ] = None,
    units: Annotated[
        UnitSystem | None, typer.Option("--units", "-u", help="Default unit system.")
    ] = None,
    theme: Annotated[
        Theme | None, typer.Option("--theme", "-t", help="Default theme.")
    ] = None,
) -> None:
    if not (location or units or theme):
        console.print("[yellow]• No configuration options specified to update.[/]")
        return

    try:
        loc = asyncio.run(_resolve_location(location)) if location else None
    except ServiceError:
        err_console.print(f"[red]✗ Could not find location '{location}'.[/]")
        raise typer.Exit(1)
    except KeyboardInterrupt:
        err_console.print("\n[red]Aborted.[/]")
        raise typer.Exit(130)

    config = Config()
    config.save(location=loc, unit_system=units, theme=theme)
    console.print("[green]✓ Configuration updated successfully.[/]")


@app.command()
def reset() -> None:
    try:
        Config().reset()
        console.print("[green]✓ Configuration reset to defaults.[/]")
    except OSError as e:
        err_console.print(f"[red]✗ Failed to reset config: {e}[/]")
        raise typer.Exit(1)


async def _resolve_location(query: str) -> Location:
    async with httpx.AsyncClient(timeout=10.0) as client:
        geocoder = GeocodingService(client, Cache())
        return await geocoder.geocode(query)
