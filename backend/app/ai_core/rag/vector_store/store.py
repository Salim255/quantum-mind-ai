# ---------------------------------------------------------------------------
# In‑memory vector database for QuantumMind AI
# ---------------------------------------------------------------------------
# This simple Python list acts as your temporary vector store.
# Each time you add a document (lesson, formula explanation, example, etc.),
# you store:
#   - the raw text
#   - its embedding vector
#   - optional metadata (like "source")
#
# Example entry:
# {
#     "text": "The Hadamard gate creates superposition...",
#     "embedding": [0.12, -0.44, 0.88, ...],
#     "source": "lesson"
# }
#
# Why a list?
# ------------
# - Easy to debug
# - Easy to print and inspect
# - Perfect for learning how RAG works
# - No external dependencies
#
# Why not a real vector DB yet?
# ------------------------------
# Because you're still building the foundations of your Quantum Learning AI.
# Once your pipeline is stable, you can replace this with:
# - FAISS (local, fast, GPU‑accelerated)
# - ChromaDB (simple, local or cloud)
# - Pinecone / Weaviate / Qdrant (cloud vector DBs)
# - PostgreSQL + pgvector (production‑grade, scalable)
#
# For now, this list is perfect for:
# - understanding embeddings
# - testing semantic search
# - validating your RAG pipeline
# - experimenting with ranking and retrieval
#
# ---------------------------------------------------------------------------
# The actual in‑memory vector store:
# ---------------------------------------------------------------------------

VECTOR_DB = []
