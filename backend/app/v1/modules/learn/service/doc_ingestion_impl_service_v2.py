from pypdf import PdfReader
from app.v1.modules.learn.service.doc_ingestion_service import DocIngestionService
from app.v1.modules.learn.dto.bookmark_dto import BookmarkDTO
from app.v1.modules.learn.dto.section_dto import SectionDTO
from app.v1.modules.learn.dto.text_dto import ContentBlockDTO
from app.v1.modules.learn.dto.image_dto import ImageDTO
from fastapi import UploadFile
import logging
import re
import fitz
import os

logger = logging.getLogger(__name__)

class DocIngestionImplServiceV2:
   def create_readers(
    self,
    file: UploadFile,
):
    pdf_bytes = file.file.read()

    pypdf_reader = PdfReader(io.BytesIO(pdf_bytes))

    pymupdf_doc = fitz.open(
        stream=pdf_bytes,
        filetype="pdf",
    )

    return pypdf_reader, pymupdf_doc
   
   def merge_section_content(
        self,
        texts: list[ContentBlockDTO],
        images: list[ImageDTO],
    ):
        merged = []

        image_lookup = {
            (
                img.bookmark_title,
                img.section_title,
            ): img
            for img in images
        }

        order = 0

        for text in texts:

            text.order = order
            merged.append(text)

            order += 1

            key = (
                text.bookmark_title,
                text.section_title,
            )

            image = image_lookup.get(key)

            if image:

                merged.append(
                    ContentBlockDTO(
                        bookmark_title=image.bookmark_title,
                        section_title=image.section_title,
                        type="figure",
                        order=order,
                        image_paths=image.image_paths,
                    )
                )

                order += 1

        return merged