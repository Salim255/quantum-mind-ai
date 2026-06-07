from sentence_transformers import CrossEncoder
from sentence_transformers import SentenceTransformer
from app.core.settings import Settings, get_settings
from app.v1.modules.rag.embeddings.embedder import RAGEmbedder
from app.db.qdrant import QdrantService
from groq import Groq
from app.db.db_engine import DBEngineService
from app.db.db_settings import DbSettingsService

class Container:
    def __init__(self):
        # ============================================================
        # CORE CONFIG (SINGLE SOURCE OF TRUTH)
        # ============================================================
        self.settings: Settings = get_settings()

        # --------------------------------------------------------
        # GROQ CLIENT (IMPORTANT: SINGLETON)
        # --------------------------------------------------------
        self.groq_client: Groq = Groq(
            api_key=self.settings.GROAI_API_KEY
        )

        # MODELS (load once)
        #self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        # Load the embedding model ONCE at module import time.
        # This avoids reloading the model on every request, which would be slow.
        # "all-MiniLM-L6-v2" is a fast, lightweight, high‑quality embedding model.
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.rag_embedder = RAGEmbedder(self.embedding_model)

        # MODELS (load once)
        # ------------------------------------------------------------
        # CROSS-ENCODER RERANKER
        # ------------------------------------------------------------
        # This model is used AFTER vector search.
        #
        # It takes (query, document) pairs and directly predicts
        # how relevant the document is to the query.
        #
        # Unlike embeddings (which are independent vectors),
        # cross-encoders look at BOTH texts together.
        #
        # This makes them MUCH more accurate, but slower.
        # ------------------------------------------------------------
        self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

        # VECTOR DB CLIENT (example)
        # QdrantClient(...)
        self.qdrant = QdrantService(settings=self.settings)

        self.db_url = DbSettingsService(settings=self.settings)
        self.db_engine = DBEngineService(db_url=self.db_url.get_sql_db_url)