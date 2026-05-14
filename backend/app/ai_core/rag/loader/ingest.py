# rag/loader/ingest.py

from app.ai_core.rag.loader.pdf_loader import load_pdf
from app.ai_core.rag.loader.chunker import chunk_text
from app.ai_core.rag.vector_store.add_document import add_document  # your existing function
from app.ai_core.rag.loader.cleaner import clean_text

def ingest_pdf(path: str):
    """
    Load a PDF, chunk it, embed each chunk, and store in VECTOR_DB.
    """

    # 1. Extract raw text from the PDF.
    full_text = load_pdf(path)

    # CLEAN THE TEXT BEFORE CHUNKING
    full_text = clean_text(full_text)
    
    # 2. Split into smaller chunks.
    chunks = chunk_text(full_text)

    # 3. Add each chunk to the vector DB.
    for chunk in chunks:
       add_document(chunk, source="document")

    return {"status": "ok", "chunks_added": len(chunks)}
