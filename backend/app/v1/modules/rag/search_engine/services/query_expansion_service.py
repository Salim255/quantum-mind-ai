from typing import List
import numpy as np
from app.v1.modules.rag.embeddings.embedder import embed_text
from app.v1.modules.rag.retriever.query_expander import expand_query

class QueryExpansionService:
    @staticmethod
    def expand(query: str) -> List[str]:
        return expand_query(query)
    
    @staticmethod
    def embed(queries: List[str]) -> List[np.ndarray]:
        return [
            np.array(embed_text(q, source="user_query")["embedding"])
            for q in queries
        ]