import asyncio
from typing import Annotated

import typer

import weather.app
from weather import __version__

app = typer.Typer()


def version_callback(value: bool) -> None:
    """Show version and exit."""
    if value:
        print(f"weather {__version__}")
        raise typer.Exit()


@app.command()
def main(
    location: Annotated[
        str | None, typer.Option("--location", "-l", help="Location")
    ] = None,
    version: Annotated[
        bool | None,
        typer.Option(
            "--version",
            callback=version_callback,
            is_eager=True,
            help="Show version and exit.",
        ),
    ] = None,
):
    asyncio.run(weather.app.run(location))
