# ---------------------------------------------------------------------------
# rag/retriever/retriever.py
# ---------------------------------------------------------------------------
# The Retriever is the component responsible for:
# - taking a user query
# - embedding it
# - performing semantic search
# - returning the most relevant text chunks
#
# It does NOT:
# - call the LLM
# - generate answers
# - validate results
# - perform reasoning
#
# It is intentionally simple and pure.
# This makes it easy to debug and perfect for learning how RAG works.
# ---------------------------------------------------------------------------

from backend.app.ai_core.rag.vector_store.search import  search_similar_documents
# Import the semantic search function.
# This function performs cosine similarity over your VECTOR_DB
# and returns the top‑K most relevant text chunks.


class Retriever:
    """
    The Retriever class is a thin wrapper around the semantic search function.
    It provides a clean interface for the rest of your RAG pipeline.
    """

    def retrieve(self, query: str):
        """
        Retrieve top‑K text chunks relevant to the user's query.

        Parameters
        ----------
        query : str
            The raw user question or text input.

        Returns
        -------
        list[str]
            A list of the most relevant text chunks.
            These chunks will later be passed to the LLM as context.
        """

        # Call the semantic search function.
        # search_similar_documents(query) returns a dictionary:
        # { "results": ["chunk1", "chunk2", ...] }
        #
        # We extract only the list of text chunks.
        return  search_similar_documents(query)["results"]
