from abc import ABC

import httpx


class Provider(ABC):
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
