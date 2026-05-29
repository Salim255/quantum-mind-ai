from qdrant_client import QdrantClient
from app.core.settings import Settings, get_settings
from typing import Annotated

class QdrantService:
    def __init__(
            self,
            settings: Annotated[Settings, get_settings]
            ):
        self.settings = settings
        
    def get_qdrant_client(self)-> QdrantClient:
        client = QdrantClient(url=self.settings.QDRANT_URL)
        return client