import typer

from weather.config import Config

app = typer.Typer(name="config", help="Manage config")


@app.command()
def path() -> None:
    print(Config().file.resolve())
