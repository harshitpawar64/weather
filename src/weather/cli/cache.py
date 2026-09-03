import typer
from rich.console import Console
from rich.table import Table

from weather.cache import Cache

app = typer.Typer(name="cache", help="Manage cache")
console = Console()


@app.command()
def path() -> None:
    print(Cache().file.resolve())


@app.command()
def stats() -> None:
    cache = Cache()
    stats = cache.stats()

    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold cyan")
    table.add_column(style="white")

    if stats.expired > 0:
        expired_str = f"{stats.expired} [dim](run 'weather cache prune' to clean)[/]"
    else:
        expired_str = "0 [dim](clean)[/]"

    table.add_row("Size:", stats.formatted_size)
    table.add_row("Queries:", str(stats.queries))
    table.add_row("Entries:", str(stats.entries))
    table.add_row("Expired:", expired_str)

    console.print(table)


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
    try:
        Cache().clear()
        typer.secho("✓ Cache cleared successfully.", fg=typer.colors.GREEN)
    except OSError as e:
        typer.secho(f"✗ Failed to clear cache: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)
