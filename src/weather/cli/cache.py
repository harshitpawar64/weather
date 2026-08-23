import typer

from weather.cache import Cache

app = typer.Typer(name="cache", help="Manage cache")


@app.command()
def path() -> None:
    print(Cache().file.resolve())


@app.command()
def prune() -> None:
    if removed := Cache().prune():
        typer.secho(
            f"✓ Pruned {removed} expired cache {'entry' if removed == 1 else 'entries'}.",
            fg=typer.colors.GREEN,
        )
    else:
        typer.secho(
            "• Cache is already clean. No expired entries found.", fg=typer.colors.BLUE
        )


@app.command()
def clear() -> None:
    Cache().clear()
    typer.secho("✓ Cache cleared successfully.", fg=typer.colors.GREEN)
