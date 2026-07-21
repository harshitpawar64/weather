import asyncio
from typing import Annotated

import typer

import weather.app
from weather import __version__
from weather.models import UnitSystem

app = typer.Typer()


def validate_units(ctx: typer.Context) -> UnitSystem:
    metric = ctx.params.get("metric", False)
    imperial = ctx.params.get("imperial", False)

    if metric and imperial:
        raise typer.BadParameter(
            "Cannot use both --metric and --imperial flags together."
        )

    if metric:
        return UnitSystem.METRIC
    if imperial:
        return UnitSystem.IMPERIAL

    return UnitSystem.METRIC


def version_callback(value: bool) -> None:
    """Show version and exit."""
    if value:
        print(f"weather {__version__}")
        raise typer.Exit()


@app.command()
def main(
    ctx: typer.Context,
    location: Annotated[
        str | None, typer.Option("--location", "-l", help="Location")
    ] = None,
    metric: Annotated[
        bool, typer.Option("--metric", help="Use metric units (°C, km/h, mm)")
    ] = False,
    imperial: Annotated[
        bool, typer.Option("--imperial", help="Use imperial units (°F, mph, in)")
    ] = False,
    json_output: Annotated[
        bool, typer.Option("--json", help="Output result in JSON format.")
    ] = False,
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
    unit_system = validate_units(ctx)
    asyncio.run(weather.app.run(location, unit_system, json_output))
