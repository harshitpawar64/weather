import logging

from rich.console import Console
from rich.logging import RichHandler


def setup_logging(verbose: bool) -> None:
    level = logging.INFO if verbose else logging.ERROR
    err_console = Console(stderr=True)

    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[
            RichHandler(
                console=err_console,
                show_time=False,
                show_path=False,
                rich_tracebacks=True,
            )
        ],
        force=True,
    )

    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
