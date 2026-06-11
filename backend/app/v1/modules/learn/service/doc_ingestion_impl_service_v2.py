from typing import List, Optional
from pydantic import BaseModel
import logging
from app.v1.modules.learn.service.doc_ingestion_service_v2 import DocIngestionServiceV2
from fastapi import UploadFile
import fitz

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

class DocIngestionImplServiceV2(DocIngestionServiceV2):

    # -------------------------
    # PUBLIC ENTRYPOINT
    # -------------------------
    async def ingest(self, file: UploadFile):
        logger.info("Starting ingestion pipeline...")

        bytes_data = await file.read()

        raw = RawDocument(
            document_id=file.filename,
            bytes_data=bytes_data,
            filename=file.filename,
            mime_type=file.content_type
        )

        pdf_obj = self.load_pdf(raw)
        #html = self._convert_pdf_to_html(pdf_obj)
       # sections = self._chunk_html(html)

       # return IngestionResult(
       #     document_id=raw.document_id,
       #     sections=sections
        #)
        print(pdf_obj)
        return  "hello world"

    # -------------------------
    # PRIVATE PIPELINE STAGES
    # -------------------------
    def load_pdf(self, raw: RawDocument):
        """
        Load PDF bytes into a PyMuPDF document object.
        """
        try:
            pdf_obj = fitz.open(stream=raw.bytes_data, filetype="pdf")
            logger.info(f"Loaded PDF '{raw.filename}' with {pdf_obj.page_count} pages")
            return pdf_obj

        except Exception:
            logger.exception("Failed to load PDF")
            raise 

    def convert_pdf_to_html(self, pdf_obj) -> str:
        """
        TODO: Implement PDF → HTML conversion (pdf2htmlEX, Grobid, etc.)
        """
        return "hello"

    def chunk_html(self, html: str) -> List[DocumentSection]:
        """
        TODO: Implement HTML chunking (headings, figures, math blocks)
        """
        return "hello"
