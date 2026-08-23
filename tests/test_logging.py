import logging

from weather.logging import setup_logging


def test_verbose() -> None:
    setup_logging(verbose=True)
    assert logging.getLogger().level == logging.INFO


def test_non_verbose() -> None:
    setup_logging(verbose=False)
    assert logging.getLogger().level == logging.ERROR
