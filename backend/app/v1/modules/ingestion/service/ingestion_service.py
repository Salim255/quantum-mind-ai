from abc import ABC, abstractmethod
from pypdf import PdfReader
from app.v1.modules.learn.dto.bookmark_dto import BookmarkDTO
from app.v1.modules.learn.dto.section_dto import SectionDTO
from app.v1.modules.learn.dto.text_dto import TextDTO
from fastapi import UploadFile
from app.v1.modules.rag.dto.chunk_dto import ChunkDTO

class DocIngestionService(ABC):
    @abstractmethod
    async def pdf_ingestion_pipeline(self, file:UploadFile ):
        raise NotImplementedError
        
    @abstractmethod
    def extract_file(self, file:UploadFile)-> PdfReader:
        raise NotImplementedError

    @abstractmethod
    def extract_bookmarks(self, reader: PdfReader) -> list[BookmarkDTO]:
        """
        Extracts the top-level bookmarks (chapters)
        and their nested sections from the PDF outline.
        """
        raise NotImplementedError
    
    @abstractmethod
    def extract_sections(
        self,
        reader: PdfReader,
        bookmarks: list[BookmarkDTO],
    ) -> list[SectionDTO]:
        """
        Converts bookmark hierarchy into explicit sections
        with page boundaries.
        """
        raise NotImplementedError

    @abstractmethod
    def extract_text(
        self,
        reader: PdfReader,
        sections: list[SectionDTO],
    ) -> list[TextDTO]:
        """
        Extracts the exact text belonging to each section.
        """
        raise NotImplementedError
        
    @abstractmethod
    def add_qdrant_document(self, chunk: ChunkDTO, source: str = "document"):
        raise NotImplementedError
