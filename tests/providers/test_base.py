from typing import ClassVar
from unittest.mock import MagicMock

import httpx
import pytest

from weather.exceptions import ProviderError
from weather.providers.base import Provider


class DummyNoKeyProvider(Provider):
    pass


class DummyKeyRequiredProvider(Provider):
    API_KEY_ENV: ClassVar[str | None] = "TEST_API_KEY"


def test_provider_without_api_key_env() -> None:
    client = MagicMock(spec=httpx.AsyncClient)
    provider = DummyNoKeyProvider(client)

    assert provider.api_key is None
    assert provider.is_configured is True


def test_provider_with_api_key_configured(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_API_KEY", "secret_123")
    client = MagicMock(spec=httpx.AsyncClient)
    provider = DummyKeyRequiredProvider(client)

    assert provider.api_key == "secret_123"
    assert provider.is_configured is True
    assert provider.required_api_key == "secret_123"


def test_provider_with_api_key_unconfigured(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TEST_API_KEY", raising=False)
    client = MagicMock(spec=httpx.AsyncClient)
    provider = DummyKeyRequiredProvider(client)

    assert provider.api_key is None
    assert provider.is_configured is False
    with pytest.raises(
        ProviderError, match="TEST_API_KEY environment variable is not set or is empty."
    ):
        _ = provider.required_api_key
