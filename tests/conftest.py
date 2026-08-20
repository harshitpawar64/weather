from collections.abc import AsyncGenerator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import httpx
import msgspec
import pytest
from typer.testing import CliRunner

import tests.constants as c
from weather.cache import Cache
from weather.config import Config
from weather.models import AirQuality, WeatherData


@pytest.fixture
def cache(tmp_path: Path) -> Cache:
    return Cache(cache_dir=tmp_path)


@pytest.fixture
def config(tmp_path: Path) -> Config:
    return Config(config_dir=tmp_path)


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def mock_client() -> MagicMock:
    return MagicMock(spec=httpx.AsyncClient)


@pytest.fixture
def mock_http_client() -> Callable[..., AbstractAsyncContextManager[httpx.AsyncClient]]:
    @asynccontextmanager
    async def _factory(
        payload: Any = None, status_code: int = 200
    ) -> AsyncGenerator[httpx.AsyncClient, None]:
        if payload is not None:
            content = (
                payload if isinstance(payload, bytes) else c.ENCODER.encode(payload)
            )
        else:
            content = b""

        transport = httpx.MockTransport(
            lambda req: httpx.Response(status_code, content=content)
        )
        async with httpx.AsyncClient(transport=transport) as client:
            yield client

    return _factory


@pytest.fixture
def make_weather() -> Callable[..., WeatherData]:
    def _factory(**overrides: Any) -> WeatherData:
        return msgspec.structs.replace(c.WEATHER_DATA, **overrides)

    return _factory


@pytest.fixture
def make_aqi() -> Callable[..., AirQuality]:
    def _factory(**overrides: Any) -> AirQuality:
        return msgspec.structs.replace(c.AIR_QUALITY, **overrides)

    return _factory
