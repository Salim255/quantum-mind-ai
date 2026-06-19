from pypdf import PdfReader
from app.v1.modules.ingestion.service.ingestion_service import DocIngestionService
from app.v1.modules.ingestion.dto.bookmark_dto import BookmarkDTO 
from app.v1.modules.ingestion.dto.section_dto import SectionDTO 
from app.v1.modules.ingestion.dto.text_dto import ContentBlockDTO
from app.v1.modules.ingestion.dto.chunker_dto import ChunkDTO
from app.v1.modules.ingestion.dto.ingestion_dto import IngestionResponseDto
from app.v1.modules.ingestion.dto.document_dto import (DocumentDTO, AddedDocResponseDto, MetadataDTO)
from app.core.container import Container
from app.db.qdrant_mapper import QdrantMapper
from app.v1.modules.ingestion.service.chunker_service import RAGChunker
from fastapi import UploadFile
import logging
import re
import asyncio
from uuid import uuid4



logger = logging.getLogger(__name__)

class DocIngestionImplService(DocIngestionService):
    def __init__(self, container: Container):
        self.container:Container = container

    async def pdf_ingestion_pipeline(self, file:UploadFile):
        try:
            # 1 extract the file
            reader:PdfReader = self.extract_file(file=file)

            print("Get pages====\n",len(reader.pages))
            logger.info("Pages: %d", len(reader.pages))
            # 2 Save doc to database

            # 3 extract_bookmarks
            extracted_bookmarks: list[BookmarkDTO] =   self.extract_bookmarks(reader=reader)
        
            # 4 extract_sections
            extracted_sections = self.extract_sections(reader=reader, bookmarks=extracted_bookmarks)

            extracted_texts = self.extract_text(
                file_name=file.filename,
                reader=reader,
                sections=extracted_sections
                )
            
            # 6 extract_images
            #merged_contents = self.merge_content_blocks(texts=extracted_texts, images=extracted_images)
            # 7 persist_to_database
            # return extracted_bookmarks
            # return extracted_sections

            chunks = RAGChunker.semantic_chunk_text(extracted__sections_texts=extracted_texts)

            return chunks

            # ------------------------------------------------------------------
            # STORE CHUNKS CONCURRENTLY
            # ------------------------------------------------------------------
            #
            # Each chunk must:
            #   1. Generate an embedding
            #   2. Be inserted into Qdrant
            #
            # Both operations are I/O-bound and support async execution.
            #
            # Instead of processing chunks one-by-one:
            #
            #   for chunk in chunks:
            #       await add_qdrant_document(...)
            #
            # we process multiple chunks concurrently to reduce total ingestion
            # time.
            #
            # ------------------------------------------------------------------
            # CONCURRENCY LIMIT
            # ------------------------------------------------------------------
            #
            # A semaphore limits the number of active insert operations.
            #
            # Without a semaphore:
            #
            #   await asyncio.gather(...)
            #
            # all chunk insertions would start immediately.
            #
            # For large documents this could create hundreds of simultaneous
            # embedding and database operations, potentially overwhelming:
            #
            #   - Qdrant
            #   - the embedding model
            #   - memory usage
            #
            # Semaphore(5) means:
            #
            #   Maximum 5 chunk insertions may run at the same time.
            #
            # When one finishes, the next waiting task is allowed to start.
            #
            # ------------------------------------------------------------------
            # SAFE WRAPPER
            # ------------------------------------------------------------------
            #
            # Every task must acquire a semaphore permit before performing the
            # insertion.
            #
            # This ensures that the concurrency limit is respected by all tasks.
            # ------------------------------------------------------------------
            sem = asyncio.Semaphore(5)
           
            async def safe_add(chunk):
                async with sem:
                    return await self.add_qdrant_document(
                        chunk,
                        source=file.filename
                    )

            # ------------------------------------------------------------------
            # CREATE TASKS
            # ------------------------------------------------------------------
            #
            # create_task() schedules all chunk insertions immediately.
            #
            # Each task runs independently and waits for a semaphore slot before
            # performing the actual work.
            # ------------------------------------------------------------------
            tasks = [
                asyncio.create_task(safe_add(chunk))
                for chunk in chunks
            ]

            # ------------------------------------------------------------------
            # WAIT FOR ALL TASKS
            # ------------------------------------------------------------------
            #
            # gather() waits until every task completes.
            #
            # The * operator unpacks the list:
            #
            #   [task1, task2, task3]
            #
            # becomes:
            #
            #   gather(task1, task2, task3)
            #
            # gather() expects separate awaitables, not a list.
            #
            # Therefore:
            #
            #   gather(*tasks)   ✅
            #
            # while:
            #
            #   gather(tasks)    ❌
            #
            # would pass a single list object instead of individual tasks.
            #
            # return_exceptions=True prevents one failed chunk from cancelling
            # all remaining chunk insertions.
            # ------------------------------------------------------------------
            await asyncio.gather(
                *tasks,
                return_exceptions=True
            )

        
                    
            
            # 4. Add each chunk to the vector DB.
            #for chunk in chunks:
            #    self.add_document_service.add_document(
            #        chunk=chunk,
            #        source=file.filename
            #    )

            # 4. Return a clean JSON response
            # -----------------------------------------------------------------------
            # This tells the client:
            # - ingestion succeeded
            # - how many chunks were added
            # - what the original filename was
            logger.info("PDF ingestion completed successfully")

            """ return IngestionResponseDto(
                status="ok",
                chunks_added=len(chunks),
                 source=file.filename
            ) """
            #return extracted_texts
            # return  extracted_bookmarks
            # return  extracted_images
            #return  merged_contents

            
        
        except Exception:
            logger.exception("Error in pdf ingestion")
            raise

    def extract_file(self, file:UploadFile) -> PdfReader:
        """
        Loads the uploaded PDF into memory.
        """

        file.file.seek(0)

        reader = PdfReader(file.file)

        logger.info("PDF loaded successfully.")
        logger.info("Pages: %s", len(reader.pages))

        return reader
        


    def extract_bookmarks(self, reader: PdfReader) -> list[BookmarkDTO]:
        """
        Extracts the top-level bookmarks (chapters)
        and their nested sections from the PDF outline.
        """
        bookmarks: list[BookmarkDTO] = []

        outline = reader.outline

        order = 1
        
        for item in outline:

            if isinstance(item, dict):

                title = item.get("/Title")

                if not title:
                    continue

                start_page = reader.get_page_number(item["/Page"]) + 1

                bookmarks.append(
                    BookmarkDTO(
                        title=title,
                        order=order,
                        start_page=start_page,
                        end_page=0,
                    )
                )

                order += 1

        # Determine end pages
        for i in range(len(bookmarks)):

            if i < len(bookmarks) - 1:
                bookmarks[i].end_page = bookmarks[i + 1].start_page - 1
            else:
                bookmarks[i].end_page = len(reader.pages)

        logger.info("Extracted %s bookmarks.", len(bookmarks))
        print("Bookmarks====\n", bookmarks)
        return bookmarks
    
    def extract_sections(
        self,
        reader: PdfReader,
        bookmarks: list[BookmarkDTO],
    ) -> list[SectionDTO]:
        """
        Extract all inner sections from the PDF outline and enrich them
        with:
        - end_page
        - next_section_title
        - next_bookmark_title

        Pages provide coarse boundaries.
        Titles provide precise boundaries.
        """

        sections: list[SectionDTO] = []

        outline = reader.outline

        current_bookmark: str | None = None

        # --------------------------------------------------
        # PASS 1: Extract raw sections
        # --------------------------------------------------
        for item in outline:

            # Top-level bookmark
            if isinstance(item, dict):
                current_bookmark = item.get("/Title")

            # Nested sections under the bookmark
            elif isinstance(item, list):

                for section in item:

                    title = section.get("/Title")

                    if not title:
                        continue

                    start_page = (
                        reader.get_page_number(section["/Page"]) + 1
                    )

                    sections.append(
                        SectionDTO(
                            bookmark_title=current_bookmark,
                            title=title,
                            start_page=start_page,
                            end_page=0,  # temporary
                            next_section_title=None,
                            next_bookmark_title=None,
                        )
                    )

        # --------------------------------------------------
        # PASS 2: Group sections by bookmark
        # --------------------------------------------------
        grouped_sections: dict[str, list[SectionDTO]] = {}

        for section in sections:
            grouped_sections.setdefault(
                section.bookmark_title,
                [],
            ).append(section)

        bookmark_lookup = {
            bookmark.title: bookmark
            for bookmark in bookmarks
        }

        bookmark_titles = [
            bookmark.title
            for bookmark in bookmarks
        ]

        # --------------------------------------------------
        # PASS 3: Compute boundaries
        # --------------------------------------------------
        for bookmark_title, bookmark_sections in grouped_sections.items():

            # Preserve PDF order
            bookmark_sections.sort(
                key=lambda section: section.start_page
            )

            for index, section in enumerate(bookmark_sections):

                # ------------------------------------------
                # Normal case:
                # next section in same bookmark
                # ------------------------------------------
                if index < len(bookmark_sections) - 1:

                    next_section = bookmark_sections[index + 1]

                    section.next_section_title = (
                        next_section.title
                    )

                    # DO NOT subtract 1.
                    # Multiple sections can share a page.
                    section.end_page = (
                        next_section.start_page
                    )

                # ------------------------------------------
                # Last section of bookmark
                # ------------------------------------------
                else:

                    bookmark = bookmark_lookup[
                        bookmark_title
                    ]

                    section.end_page = (
                        bookmark.end_page
                    )

                    current_index = bookmark_titles.index(
                        bookmark_title
                    )

                    if current_index < len(bookmark_titles) - 1:

                        section.next_bookmark_title = (
                            bookmark_titles[
                                current_index + 1
                            ]
                        )

        logger.info(
            "Extracted %s sections.",
            len(sections),
        )

        return sections


    def _get_next_bookmark_title(self, current, bookmarks):
        for i, b in enumerate(bookmarks):
            if b.title == current.title and i < len(bookmarks) - 1:
                return bookmarks[i + 1].title
        return None

    def extract_between_titles(
        self,
        text: str,
        current_title: str,
        next_title: str | None,
    ) -> str:
        """
        Extract text starting from the current section title
        and ending just before the next section title.
        """

        # -----------------------------
        # Find current section header
        # -----------------------------
        start_pattern = (
            rf"(?im)^\s*{re.escape(current_title)}\s*$"
        )

        start_match = re.search(start_pattern, text)

        if not start_match:
            return ""

        text = text[start_match.start():]

        # -----------------------------
        # Find next section header
        # -----------------------------
        if next_title:

            end_pattern = (
                rf"(?im)^\s*{re.escape(next_title)}\s*$"
            )

            end_match = re.search(end_pattern, text)

            if end_match:
                text = text[:end_match.start()]

        return text.strip()


    def extract_text(
        self,
        file_name: str,
        reader: PdfReader,
        sections: list[SectionDTO]
    ) -> list[ContentBlockDTO]:

        texts: list[ContentBlockDTO] = []

        total_pages = len(reader.pages)

        sections = sorted(sections, key=lambda s: s.start_page)

        order = 1
        
        for section in sections:

            start_page = max(1, min(section.start_page, total_pages))
            end_page = max(start_page, min(section.end_page, total_pages))

            page_texts: list[str] = []

            

            # Extract raw text from the section pages
            for page_num in range(start_page, end_page + 1):
                page = reader.pages[page_num - 1]

                text = page.extract_text()

                if text:
                    page_texts.append(text)

            raw_text = "\n".join(page_texts)

            # Use the next section title already stored in the DTO
            clean_text = self.extract_between_titles(
                text=raw_text,
                current_title=section.title,
                next_title=section.next_section_title,
            )

            # NEW STEP (safe place for cleanup section.title)
            clean_text = clean_text.replace(section.title, "", 1).strip()
            
            texts.append(
                ContentBlockDTO(
                    bookmark_title=section.bookmark_title,
                    section_title=section.title,
                    order=order,
                    content=clean_text,
                    source_name=file_name
                )
            )

            order += 1
            if order==5:
                return texts
        return texts
    

    async def add_qdrant_document(self, chunk: ChunkDTO, source: str = "document"):
        """
        Add a document to the QuantumMind AI vector store.

        Parameters
        ----------
        text : str
            The raw text content to store and embed.
            This can be a lesson, explanation, formula description,
            or any quantum learning material.

        source : str
            A tag describing the origin of the content.
            Helps the retriever prioritize and rank results.
            Defaults to "document".

        Returns
        -------
        dict
            A simple status dictionary confirming the operation.
        """

        # --- 1. Generate an embedding for the provided text ----------------------
        # The embed_text() tool returns a dictionary:
        # { "embedding": [...], "normalize": True, "source": "lesson" }
        # We extract only the vector because that's what we store in the DB.
        # 1. Extract text safely
        # text = chunk["text"] if isinstance(chunk, dict) else chunk
        embedding_result = self.container.rag_embedder.embed_text(text=chunk.content, source=chunk.source_name)

        emb = embedding_result["embedding"]


        # --- 2. Build the document entry ----------------------------------------
        document_entry = DocumentDTO(
            text=chunk.content,
            embedding=emb,
            metadata=MetadataDTO(
                source=source,
                concept=chunk.section_title,
                length=chunk.length
            )
        )


        # --- 3. Save the entry in the in-memory vector DB -----------------------
        await self.container.qdrant.client.upsert(
            collection_name="documents",
            points=[
                QdrantMapper.to_point(
                    doc=document_entry,
                    point_id = str(uuid4())
                )
            ]
        )

        #self.container.qdrant.client.scroll(
        #    collection_name="documents",
        #    limit=1,
        #    with_vectors=True
        #)

    
        # --- 4. Return a confirmation -------------------------------------------
        # The agent_core expects a JSON-serializable response.
        return AddedDocResponseDto(
                status="ok",
                stored_text_length=len(chunk.content),
                source=source
            )