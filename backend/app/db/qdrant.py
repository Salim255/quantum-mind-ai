import logging
from qdrant_client import AsyncQdrantClient
from app.core.settings import Settings
from qdrant_client.models import Distance, VectorParams

logger = logging.getLogger(__name__)

class QdrantService:
    def __init__(self, settings: Settings):
        self.settings = settings
    
        self._client = AsyncQdrantClient(url=self.settings.QDRANT_URL, timeout=120) # CREATE ONCE

    async def create_collection(self):
        try:
            await self._client.create_collection(
                collection_name=self.settings.COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=self.settings.VECTOR_SIZE,  # your embedding model size
                    distance=Distance.COSINE
                )
            )

        except Exception:
            logger.exception("Create doc failed")
      
    @property
    def client(self)-> AsyncQdrantClient:

        return self._client
    
    async def close(self):
        await self._client.close()