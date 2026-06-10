from pypdf import PdfReader
from app.v1.modules.learn.service.doc_ingestion_service import DocIngestionService
from app.v1.modules.learn.dto.bookmark_dto import BookmarkDTO
from app.v1.modules.learn.dto.section_dto import SectionDTO
from app.v1.modules.learn.dto.text_dto import TextDTO
from app.v1.modules.learn.dto.image_dto import ImageDTO
from fastapi import UploadFile
import logging
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

            #extracted_texts = self.extract_text(reader=reader, sections=extracted_sections)
            # 6 extract_images
            #extracted_images = self.extract_images()
            # 7 persist_to_database
            # return extracted_bookmarks
            return extracted_sections
            # return extracted_texts
        
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

        # STEP 1: flatten all outline items into (title, page)
        flat_items = []

        def walk(items):
            for item in items:
                if isinstance(item, dict):
                    title = item.get("/Title")
                    page = reader.get_page_number(item["/Page"]) + 1

                    if title and page:
                        flat_items.append({
                            "title": title,
                            "page": page
                        })

                elif isinstance(item, list):
                    walk(item)

        walk(reader.outline)

        # STEP 2: assign sections to bookmarks by page range
        for bookmark in bookmarks:

            # get sections inside this bookmark range
            bookmark_sections = [
                x for x in flat_items
                if bookmark.start_page <= x["page"] <= bookmark.end_page
                and x["title"] != bookmark.title
            ]

            # STEP 3: build SectionDTOs
            for i, sec in enumerate(bookmark_sections):

                next_section_title = None
                next_section_page = None
                next_bookmark_title = None

                if i < len(bookmark_sections) - 1:
                    next_section_title = bookmark_sections[i + 1]["title"]
                    next_section_page = bookmark_sections[i + 1]["page"]
                else:
                    next_bookmark_title = self._get_next_bookmark_title(bookmark, bookmarks)

                sections.append(
                    SectionDTO(
                        bookmark_title=bookmark.title,
                        title=sec["title"],
                        start_page=sec["page"],
                        next_section_title=next_section_title,
                        next_section_page=next_section_page,
                        next_bookmark_title=next_bookmark_title,
                    )
                )

        return sections


    def _get_next_bookmark_title(self, current, bookmarks):
        for i, b in enumerate(bookmarks):
            if b.title == current.title and i < len(bookmarks) - 1:
                return bookmarks[i + 1].title
        return None

    def extract_text(
        self,
        reader: PdfReader,
        sections: list[SectionDTO],
    ) -> list[TextDTO]:
        """
        Extracts the exact text belonging to each section.
        """
            
        texts: list[TextDTO] = []

        for section in sections:

            content_parts: list[str] = []

            for page_number in range(
                section.start_page,
                section.end_page + 1,
            ):

                page = reader.pages[page_number - 1]

                page_text = page.extract_text()

                if page_text:
                    content_parts.append(page_text)

            texts.append(
                TextDTO(
                    bookmark_title=section.bookmark_title,
                    section_title=section.title,
                    content="\n".join(content_parts),
                )
            )

        logger.info("Extracted text for %s sections.", len(texts))

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