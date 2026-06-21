from typing import List
import numpy as np
import time
from fastapi import Request
from app.core.container import Container
from concurrent.futures import ThreadPoolExecutor

class EmbeddingService:
    def __init__(self, container: Container):
        self.container:Container = container
    
    def query_embeder(self, query: str):
        return np.array(
            self.container.rag_embedder.embed_text(
                text=query,
                source="user_query"
            )["embedding"]
        )

        #Perfoamnce check=====
        #2.105046750046313
    
    def embed_expanded_queries(
        self,
        expanded_queries: List[str]
        ) -> List[np.ndarray]:
        """
        Convert expanded queries into embedding vectors.

        RETURNS
        -------
        List[np.ndarray]

        Example:
        --------
        [
            [0.12, 0.44, 0.91],
            [0.66, 0.28, 0.77],
            [0.31, 0.85, 0.55]
        ]

        WHY IMPORTANT?
        --------------
        Embeddings convert semantic meaning into vector space,
        enabling mathematical similarity comparison.
        """
        return [
           self.query_embeder(query=query)
           for query in expanded_queries
        ]
       
    
