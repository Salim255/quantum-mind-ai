from qdrant_client import QdrantClient
from app.core.settings import Settings, get_settings
from typing import Annotated

class QdrantService:
    def __init__(self, qdrant_url: str):
        self.qdrant_url = qdrant_url
        self._client = QdrantClient(url=self.qdrant_url) # CREATE ONCE

    @property
    def client(self)-> QdrantClient:

        return self._client