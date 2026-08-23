import asyncio
import logging
from typing import Annotated

import typer

from weather import __version__
from weather.cli import cache, config, setup
from weather.exceptions import WeatherError
from weather.logging import setup_logging
from weather.models import Theme, UnitSystem

logger = logging.getLogger(__name__)

app = typer.Typer()

app.add_typer(setup.app)
app.add_typer(cache.app)
app.add_typer(config.app)


def resolve_units(metric: bool, imperial: bool) -> UnitSystem | None:
    if metric and imperial:
        raise typer.BadParameter(
            "Cannot use both --metric and --imperial flags together."
        )

    if metric:
        return UnitSystem.METRIC
    if imperial:
        return UnitSystem.IMPERIAL

    return None


def version_callback(value: bool) -> None:
    """Show version and exit."""
    if value:
        print(f"weather {__version__}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    location: Annotated[
        str | None, typer.Option("--location", "-l", help="Location")
    ] = None,
    theme: Annotated[
        Theme | None,
        typer.Option("--theme", "-t", help="Theme to use for rendering output."),
    ] = None,
    days: Annotated[
        int,
        typer.Option(
            "--days",
            "-d",
            min=1,
            max=16,
            help="Total days of forecast, including today.",
        ),
    ] = 7,
    metric: Annotated[
        bool, typer.Option("--metric", help="Use metric units (°C, km/h, mm)")
    ] = False,
    imperial: Annotated[
        bool, typer.Option("--imperial", help="Use imperial units (°F, mph, in)")
    ] = False,
    json_output: Annotated[
        bool, typer.Option("--json", help="Output result in JSON format.")
    ] = False,
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="Verbose logging output.")
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
    setup_logging(verbose)

    if ctx.invoked_subcommand:
        return

    unit_system = resolve_units(metric, imperial)

    import weather.app

    try:
        asyncio.run(weather.app.run(location, unit_system, theme, days, json_output))
    except WeatherError as e:
        logger.error("%s", e)
        raise typer.Exit(1)
    except KeyboardInterrupt:
        typer.secho("\nAborted.", fg=typer.colors.RED, err=True)
        raise typer.Exit(130)
