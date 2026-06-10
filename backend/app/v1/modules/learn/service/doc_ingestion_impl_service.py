from pypdf import PdfReader
from app.v1.modules.learn.service.doc_ingestion_service import DocIngestionService
from app.v1.modules.learn.dto.bookmark_dto import BookmarkDTO
from app.v1.modules.learn.dto.section_dto import SectionDTO
from app.v1.modules.learn.dto.text_dto import TextDTO
from app.v1.modules.learn.dto.image_dto import ImageDTO
from fastapi import UploadFile
import logging
import re

logger = logging.getLogger(__name__)

class DocIngestionImplService(DocIngestionService):
    def pdf_ingestion_pipeline(self, file:UploadFile):
        try:
            # 1 extract the file
            reader:PdfReader = self.extract_file(file=file)

            # 2 Save doc to database

            # 3 extract_bookmarks
            extracted_bookmarks: list[BookmarkDTO] =   self.extract_bookmarks(reader=reader)

            # 4 extract_sections
            extracted_sections = self.extract_sections(reader=reader, bookmarks=extracted_bookmarks)

            extracted_texts = self.extract_text(reader=reader, sections=extracted_sections)
            # 6 extract_images
            #extracted_images = self.extract_images()
            # 7 persist_to_database
            # return extracted_bookmarks
            #return extracted_sections
            return extracted_texts
        
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

        sections: list[SectionDTO] = []

        outline = reader.outline

        current_bookmark = None

        for item in outline:

            if isinstance(item, dict):
                current_bookmark = item.get("/Title")

            elif isinstance(item, list):

                for i, section in enumerate(item):

                    title = section.get("/Title")
                    start_page = reader.get_page_number(section["/Page"]) + 1

                    sections.append(
                        SectionDTO(
                            bookmark_title=current_bookmark,
                            title=title,
                            start_page=start_page,
                            end_page=0,  # temp
                        )
                    )

        # sort (VERY IMPORTANT)
        sections.sort(key=lambda s: s.start_page)

        # compute end_page using NEXT section
        for i in range(len(sections)):

            if i < len(sections) - 1:
                sections[i].end_page = sections[i + 1].start_page - 1
            else:
                sections[i].end_page = max(b.end_page for b in bookmarks if b.title == sections[i].bookmark_title)

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

        start = text.find(current_title)

        if start == -1:
            return ""

        text = text[start:]

        if next_title:
            end = text.find(next_title)

            if end != -1:
                text = text[:end]

        return text.strip()

    def extract_text(
        self,
        reader: PdfReader,
        sections: list[SectionDTO]
    ) -> list[TextDTO]:

        texts: list[TextDTO] = []
        total_pages = len(reader.pages)

        sections = sorted(sections, key=lambda s: s.start_page)

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

            texts.append(
                TextDTO(
                    bookmark_title=section.bookmark_title,
                    section_title=section.title,
                    content=clean_text,
                )
            )

        return texts
    
    def extract_images(
        self,
        pdf_bytes: bytes,
        sections: list[SectionDTO],
    ) -> list[ImageDTO]:
        """
        Extracts figures, equations, and circuit images
        associated with each section.
        """
    
    def persist_to_database(self):
        return ""