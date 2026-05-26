import os
import asyncio
import uuid
from fastapi import  UploadFile
import aiofiles
from app.core.container import Container
from app.v1.modules.rag.loader.chunker import RAGChunker
from app.v1.modules.rag.loader.cleaner import clean_text
from app.v1.modules.rag.loader.pdf_loader import load_pdf
from app.v1.modules.rag.services.interfaces.loader_service import LoaderService
from app.v1.modules.rag.vector_store.add_document import RAGAddDocument
from app.ai_core.structured_outputs.schemas.ingestion_schema import IngestionResponseSchema  # your existing function


class LoaderServiceImpl(LoaderService):
    def __init__(
            self, 
            container: Container, 
            add_document_service: RAGAddDocument
        ):
        self.container:Container = container
        self.add_document_service: RAGAddDocument = add_document_service

    async def upload_and_ingest_pdf(
        self,
        file: UploadFile,
        ) -> IngestionResponseSchema:
        """
        Receive a PDF file from the client (Postman, UI, etc.),
        save it asynchronously, then ingest it into the vector store.

        Parameters
        ----------
        file : UploadFile
            The uploaded PDF file sent by the client.

        Returns
        -------
        IngestionResponseSchema
            A structured response confirming ingestion and showing how many chunks were added.
        """

        # -----------------------------------------------------------------------
        # 1. Generate a unique temporary filename
        # -----------------------------------------------------------------------
        # uuid4() ensures no filename collisions, even with concurrent uploads.
        # /tmp is the correct directory for temporary files in containers.
        temp_filename = f"{uuid.uuid4()}.pdf"
        temp_path = os.path.join("/tmp", temp_filename)

    
        # -----------------------------------------------------------------------
        # 2. Save the uploaded file asynchronously
        # -----------------------------------------------------------------------
        # aiofiles ensures we do NOT block the FastAPI event loop.
        # This is the modern, recommended way to handle file writes in async apps.
        async with aiofiles.open(temp_path, "wb") as out_file:
            # Read the uploaded file content asynchronously
            content = await file.read()
            # Write the content asynchronously to the temp file
            await out_file.write(content)


        # -----------------------------------------------------------------------
        # 3. Ingest the PDF into your vector database
        # -----------------------------------------------------------------------
        # ingest_pdf() handles:
        # - extracting text
        # - chunking
        # - embedding
        # - storing chunks in VECTOR_DB
    
        # We run this in a separate thread to avoid blocking the event loop,
        # since ingest_pdf is CPU-bound and not async.
        result = await asyncio.to_thread(self.process_pdf, temp_path, source=file.filename)

        # 4. Return a clean JSON response
        # -----------------------------------------------------------------------
        # This tells the client:
        # - ingestion succeeded
        # - how many chunks were added
        # - what the original filename was
        return result

    def process_pdf(self, path: str, source: str) -> IngestionResponseSchema:
        """
        Load a PDF, chunk it, embed each chunk, and store in VECTOR_DB.
         """

        # 1. Extract raw text from the PDF.
        full_text = load_pdf(path)

        # 2. CLEAN THE TEXT BEFORE CHUNKING
        full_text = clean_text(text=full_text)

        # 3. Split into smaller chunks.
        chunks = RAGChunker.semantic_chunk_text(normalized_text=full_text)

        # 4. Add each chunk to the vector DB.
        for chunk in chunks:
            self.add_document_service.add_document(
                chunk=chunk,
                source=source
            )

        return IngestionResponseSchema(
            status="ok",
            chunks_added=len(chunks),
            source=source
        )