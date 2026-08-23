import asyncio

import typer

app = typer.Typer(name="setup", help="Run interactive onboarding setup")


@app.callback(invoke_without_command=True)
def main() -> None:
    """Run interactive onboarding setup"""
    import weather.app

    try:
        asyncio.run(weather.app.run_setup())
    except KeyboardInterrupt:
        typer.secho("\nAborted.", fg=typer.colors.RED, err=True)
        raise typer.Exit(130)
