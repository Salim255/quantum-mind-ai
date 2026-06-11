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
   
   def pdf_ingestion_pipeline(
        self,
        file: UploadFile,
    ):

        reader, pdf = self.create_readers(file)

        bookmarks = self.extract_bookmarks(reader)

        sections = self.extract_sections(
            reader=reader,
            bookmarks=bookmarks,
        )

        texts = self.extract_text_blocks(
            reader=reader,
            sections=sections,
        )

        images = self.render_section_pages(
            pdf=pdf,
            sections=sections,
        )

        contents = self.merge_section_content(
            texts=texts,
            images=images,
        )

        return contents
   
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
   

   def extract_sections(
        self,
        reader: PdfReader,
        bookmarks: list[BookmarkDTO],
    ) -> list[SectionDTO]:

        sections: list[SectionDTO] = []

        outline = reader.outline

        current_bookmark = None

        for item in outline:

            if isinstance(item, dict):
                current_bookmark = item.get("/Title")

            elif isinstance(item, list):

                for section in item:

                    title = section.get("/Title")

                    start_page = (
                        reader.get_page_number(section["/Page"]) + 1
                    )

                    sections.append(
                        SectionDTO(
                            bookmark_title=current_bookmark,
                            title=title,
                            start_page=start_page,
                            end_page=0,  # temporary
                        )
                    )

        sections.sort(key=lambda s: s.start_page)

        for i in range(len(sections)):

            current = sections[i]

            if i < len(sections) - 1:

                next_section = sections[i + 1]

                current.end_page = max(
                    current.start_page,
                    next_section.start_page,
                )

                current.next_section_title = next_section.title

            else:

                bookmark = next(
                    (
                        b
                        for b in bookmarks
                        if b.title == current.bookmark_title
                    ),
                    None,
                )

                if bookmark:
                    current.end_page = bookmark.end_page
                else:
                    current.end_page = current.start_page

        return sections
   
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