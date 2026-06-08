import logging
from groq import Groq
from app.db.qdrant import QdrantService
from sentence_transformers import CrossEncoder
from app.core.settings import SettingsService
from app.db.db_engine import DBEngineService
from app.db.db_settings import DbSettingsService
from app.db.db_session import DBSessionService
from sentence_transformers import SentenceTransformer
from app.v1.modules.rag.embeddings.embedder import RAGEmbedder
from app.db.db_init import DBInitService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

class Container:
    def __init__(self):
        # ============================================================
        # CORE CONFIG (SINGLE SOURCE OF TRUTH)
        # ============================================================

        # ============================================================
        # APPLICATION SETTINGS
        # ============================================================
        self.settings = SettingsService()

        # ============================================================
        # DATABASE CONFIGURATION
        # ============================================================
        self.db_settings = DbSettingsService(
            settings=self.settings
        )

        # ============================================================
        # DATABASE ENGINE
        # ============================================================
        self.db_engine_service = DBEngineService(
            db_url=self.db_settings.sql_db_url
        )

        self.db_session =  DBSessionService()

        self.db_init_service = DBInitService(engine=self.db_engine_service.get_engine)

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