import os
from abc import ABC
from typing import ClassVar

import httpx

from weather.exceptions import ProviderError


class Provider(ABC):
    API_URL: ClassVar[str] = ""
    API_KEY_ENV: ClassVar[str | None] = None

    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client

    @property
    def api_key(self) -> str | None:
        return os.environ.get(self.API_KEY_ENV) if self.API_KEY_ENV else None

    @property
    def is_configured(self) -> bool:
        return True if self.API_KEY_ENV is None else bool(self.api_key)

    @property
    def required_api_key(self) -> str:
        if not self.api_key:
            raise ProviderError(
                f"{self.API_KEY_ENV} environment variable is not set or is empty."
            )

        return self.api_key
