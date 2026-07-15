from typing import Annotated

import typer

from weather import __version__

app = typer.Typer()


def version_callback(value: bool):
    """Show version and exit."""
    if value:
        print(f"weather {__version__}")
        raise typer.Exit()


@app.command()
def main(
    version: Annotated[
        bool | None, typer.Option("--version", callback=version_callback, is_eager=True)
    ] = None,
): ...
