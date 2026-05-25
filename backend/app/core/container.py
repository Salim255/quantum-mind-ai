from app.core.settings import Settings, get_settings
from groq import Groq

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
        #self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")

        # VECTOR DB CLIENT (example)
        # self.vector_db = QdrantClient(...)