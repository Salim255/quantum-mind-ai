from app.v1.modules.rag.loader.chunker import semantic_chunk_text
from app.v1.modules.rag.loader.cleaner import clean_text
from app.v1.modules.rag.loader.normalizer import normalize_text
from app.v1.modules.rag.loader.pdf_loader import load_pdf
from app.v1.modules.rag.services.interfaces.loader_service import LoaderService
from app.v1.modules.rag.vector_store.add_document import add_document
from app.ai_core.structured_outputs.schemas.ingestion_schema import IngestionResponseSchema  # your existing function


class LoaderServiceImpl(LoaderService):
    def ingest_pdf(self, path: str, source: str) -> IngestionResponseSchema:
        """
        Load a PDF, chunk it, embed each chunk, and store in VECTOR_DB.
         """

        # 1. Extract raw text from the PDF.
        full_text = load_pdf(path)

        # CLEAN THE TEXT BEFORE CHUNKING
        full_text = clean_text(full_text)
        normalized = normalize_text(full_text)  # fix structure
        # 2. Split into smaller chunks.
        chunks = semantic_chunk_text(normalized)

        # 3. Add each chunk to the vector DB.
        for chunk in chunks:
            text = chunk.lower()
            # FILTER STEP (replacement for is_useful_chunk)
            if len(chunk) < 80:
                continue

            if "acknowledgements" in text:
                continue
            if "mit press" in text:
                continue
            if "all rights reserved" in text:
                continue
            if "introduction introduction" in text:
                continue
            add_document(chunk, source=source)

        return IngestionResponseSchema(
            status="ok",
            chunks_added=len(chunks),
            source=source
        )