from typing import List, Optional
from pydantic import BaseModel
import logging
from app.v1.modules.learn.service.doc_ingestion_service_v2 import DocIngestionServiceV2
from fastapi import UploadFile
import fitz
from bs4 import BeautifulSoup
import uuid

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
        html = self.convert_pdf_to_html(pdf_obj)
        sections = self.chunk_html(html)

       # return IngestionResult(
       #     document_id=raw.document_id,
       #     sections=sections
        #)
        print(html)
        return sections

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
        Convert PDF to HTML using PyMuPDF (fitz).
        This preserves:
        - figures
        - math equations (as images)
        - tables
        - layout
        """

        try:
            html_parts = []

            for i in range(pdf_obj.page_count):
                page = pdf_obj.load_page(i)
                page_html = page.get_text("html")

                wrapped = f"""
                <div class="pdf-page" data-page="{i+1}">
                    <!-- PAGE {i+1} -->
                    {page_html}
                </div>
                """

                html_parts.append(wrapped)

            return "\n".join(html_parts)

        except Exception:
            logger.exception("Failed to convert PDF to HTML")
            raise 


    def chunk_html(self, html: str) -> List[DocumentSection]:
        soup = BeautifulSoup(html, "html.parser")

        # Select each page wrapper
        pages = soup.select(".pdf-page")

        sections = []
        for order, page in enumerate(pages):
            section_id = str(uuid.uuid4())

            sections.append(
                DocumentSection(
                    section_id=section_id,
                    title=f"Page {order + 1}",
                    html=str(page),
                    order=order
                )
            )

        return sections


