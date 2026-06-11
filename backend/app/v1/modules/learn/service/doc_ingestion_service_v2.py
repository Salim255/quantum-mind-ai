from typing import List, Optional
from pydantic import BaseModel
from abc import ABC, abstractmethod
import logging
from fastapi import UploadFile

logger = logging.getLogger(__name__)


# =========================
# DOMAIN MODELS
# =========================

class DocumentSection(BaseModel):
    section_id: str
    title: Optional[str] = ""
    html: str
    order: int


class IngestionResult(BaseModel):
    document_id: str
    sections: List[DocumentSection]


class RawDocument(BaseModel):
    document_id: str
    bytes_data: bytes
    filename: str
    mime_type: str = "application/pdf"


# =========================
# ABSTRACT CONTRACT
# =========================

class DocIngestionServiceV2(ABC):

    # ---- PUBLIC ENTRYPOINT ----
    @abstractmethod
    async def ingest(self, file: UploadFile):
        """Full pipeline: load → convert → chunk → return."""
        raise NotImplementedError

    # ---- PIPELINE STAGES ----
    @abstractmethod
    def load_pdf(self, raw: RawDocument):
        """Load PDF bytes into a backend-specific PDF object."""
        raise NotImplementedError

    @abstractmethod
    def convert_pdf_to_html(self, pdf_obj) -> str:
        """Convert PDF to HTML while preserving layout, figures, math, tables."""
        raise NotImplementedError

    @abstractmethod
    def chunk_html(self, html: str) -> List[DocumentSection]:
        """Split HTML into semantic sections."""
        raise NotImplementedError
