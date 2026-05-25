from typing import List
import numpy as np
from fastapi import Request
from app.v1.modules.rag.retriever.query_expander import expand_query
from app.core.container import Container

class QueryExpansionService:
    def __init__(self, request: Request):
        self.container:Container = request.app.state.container
     
    @staticmethod
    def expand(query: str) -> List[str]:
        return expand_query(query)
    
    @staticmethod
    def embed(self, queries: List[str]) -> List[np.ndarray]:
     
        return [
            np.array(self.container.embed_text(q, source="user_query")["embedding"])
            for q in queries
        ]