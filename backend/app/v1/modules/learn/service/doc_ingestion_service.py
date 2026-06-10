from abc import ABC, abstractmethod
from pypdf import PdfReader

class DocIngestionService(ABC):
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
    ) -> list[SectionTextDTO]:
        """
        Extracts the exact text belonging to each section.
        """
        raise NotImplementedError
    
    @abstractmethod
    def extract_images(
        self,
        pdf_bytes: bytes,
        sections: list[SectionDTO],
    ) -> list[SectionImageDTO]:
        """
        Extracts figures, equations, and circuit images
        associated with each section.
        """
        raise NotImplementedError
    
    @abstractmethod
    def persist_to_database(self):
        raise NotImplementedError
