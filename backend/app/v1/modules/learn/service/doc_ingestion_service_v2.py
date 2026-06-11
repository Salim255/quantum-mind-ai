from typing import List, Literal
from pydantic import BaseModel
import fitz  # PyMuPDF
import logging
from abc import ABC, abstractmethod
logger = logging.getLogger(__name__)


# =========================
# DTOs (your final output)
# =========================

class ContentBlockDTO(BaseModel):
    bookmark_title: str
    section_title: str
    type: Literal["text", "visual"]
    order: int
    content: str | None = None
    image_path: list[str] | None = None
    caption: str | None = None


class SectionDTO(BaseModel):
    bookmark_title: str
    title: str
    start_page: int
    end_page: int


# =========================
# SERVICE
# =========================

class DocIngestionServiceV2(ABC):

    # -------------------------
    # MAIN PIPELINE
    # -------------------------
    @abstractmethod
    def pdf_ingestion_pipeline(self, file) -> list[ContentBlockDTO]:
        raise NotImplementedError

    # =========================================================
    # 1. SECTION EXTRACTION (simple + safe fallback)
    # =========================================================
    @abstractmethod
    def extract_sections(self, pdf: fitz.Document) -> List[SectionDTO]:
        raise NotImplementedError


    # =========================================================
    # 2. TEXT BLOCKS (ORDER PRESERVED)
    # =========================================================
    @abstractmethod
    def extract_text_blocks(
        self,
        pdf: fitz.Document,
        sections: List[SectionDTO],
    ) -> List[ContentBlockDTO]:
        raise NotImplementedError
        


    # =========================================================
    # 3. VISUAL BLOCKS (PAGE RENDERING)
    # =========================================================
    @abstractmethod
    def extract_visual_blocks(
        self,
        pdf: fitz.Document,
        sections: List[SectionDTO],
    ) -> List[ContentBlockDTO]:
        raise NotImplementedError

    # =========================================================
    # 4. MERGE FINAL OUTPUT
    # =========================================================
    @abstractmethod
    def merge_content_blocks(
        self,
        text_blocks: List[ContentBlockDTO],
        visual_blocks: List[ContentBlockDTO],
    ) -> List[ContentBlockDTO]:
        raise NotImplementedError