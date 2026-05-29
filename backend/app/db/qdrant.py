from qdrant_client import QdrantClient
from app.core.settings import Settings, get_settings
from qdrant_client.models import Distance, VectorParams

class QdrantService:
    def __init__(self, settings: Settings):
        self.settings = settings
    
        self._client = QdrantClient(url=self.settings.QDRANT_URL, timeout=120) # CREATE ONCE

        self.create_collection()

    def create_collection(self):
        try:
            self._client.create_collection(
                collection_name=self.settings.COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=self.settings.VECTOR_SIZE,  # your embedding model size
                    distance=Distance.COSINE
                )
            )
        except Exception as e:
            print(e)
      

    @property
    def client(self)-> QdrantClient:

        return self._client