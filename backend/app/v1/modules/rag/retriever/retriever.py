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

from app.v1.modules.rag.vector_store.search import  search_similar_documents
from app.v1.modules.rag.dto.retrieval_dto import RetrievalResponseDTO

def retrieve(query: str) -> RetrievalResponseDTO:
    """
    Retrieves relevant chunks of information based on the input query.

    Parameters
    ----------
    query : str
        The natural language question or query for which relevant information is to be retrieved.

    Returns
    -------
    RetrievalResultSchema
        The structured retrieval results containing the retrieved chunks and their associated sources.
    """
    return search_similar_documents(query)
