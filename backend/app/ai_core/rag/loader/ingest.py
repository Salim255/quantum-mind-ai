# rag/loader/ingest.py

from rag.loader.pdf_loader import load_pdf
from rag.loader.chunker import chunk_text
from rag.vector_store.store import VECTOR_DB
from rag.embeddings.embedder import embed_text
from rag.vector_store.add_document import add_document  # your existing function

def ingest_pdf(path: str):
    """
    Load a PDF, chunk it, embed each chunk, and store in VECTOR_DB.
    """

    # 1. Extract raw text from the PDF.
    full_text = load_pdf(path)

    # 2. Split into smaller chunks.
    chunks = chunk_text(full_text)

    # 3. Add each chunk to the vector DB.
    for chunk in chunks:
        add_document(chunk, source="document")

    return {"status": "ok", "chunks_added": len(chunks)}
