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
            ##extracted_texts = self.extract_text(reader=reader, sections=extracted_sections)
            # 6 extract_images
            #extracted_images = self.extract_images()
            # 7 persist_to_database
            return extracted_bookmarks
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
        """
        Converts bookmark hierarchy into explicit sections
        with page boundaries.
        """
        return ""

    def extract_text(
        self,
        reader: PdfReader,
        sections: list[SectionDTO],
    ) -> list[TextDTO]:
        """
        Extracts the exact text belonging to each section.
        """
        return ""
    
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