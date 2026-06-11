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
            #extracted_images = self.extract_images(file=file, sections=extracted_sections)
            # 7 persist_to_database
            # return extracted_bookmarks
            #return extracted_sections
            return extracted_texts
            #return  extracted_images
        
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
        Extract all inner sections from the PDF outline and enrich them
        with:
        - end_page
        - next_section_title
        - next_bookmark_title

        Pages provide coarse boundaries.
        Titles provide precise boundaries.
        """

        sections: list[SectionDTO] = []

        outline = reader.outline

        current_bookmark: str | None = None

        # --------------------------------------------------
        # PASS 1: Extract raw sections
        # --------------------------------------------------
        for item in outline:

            # Top-level bookmark
            if isinstance(item, dict):
                current_bookmark = item.get("/Title")

            # Nested sections under the bookmark
            elif isinstance(item, list):

                for section in item:

                    title = section.get("/Title")

                    if not title:
                        continue

                    start_page = (
                        reader.get_page_number(section["/Page"]) + 1
                    )

                    sections.append(
                        SectionDTO(
                            bookmark_title=current_bookmark,
                            title=title,
                            start_page=start_page,
                            end_page=0,  # temporary
                            next_section_title=None,
                            next_bookmark_title=None,
                        )
                    )

        # --------------------------------------------------
        # PASS 2: Group sections by bookmark
        # --------------------------------------------------
        grouped_sections: dict[str, list[SectionDTO]] = {}

        for section in sections:
            grouped_sections.setdefault(
                section.bookmark_title,
                [],
            ).append(section)

        bookmark_lookup = {
            bookmark.title: bookmark
            for bookmark in bookmarks
        }

        bookmark_titles = [
            bookmark.title
            for bookmark in bookmarks
        ]

        # --------------------------------------------------
        # PASS 3: Compute boundaries
        # --------------------------------------------------
        for bookmark_title, bookmark_sections in grouped_sections.items():

            # Preserve PDF order
            bookmark_sections.sort(
                key=lambda section: section.start_page
            )

            for index, section in enumerate(bookmark_sections):

                # ------------------------------------------
                # Normal case:
                # next section in same bookmark
                # ------------------------------------------
                if index < len(bookmark_sections) - 1:

                    next_section = bookmark_sections[index + 1]

                    section.next_section_title = (
                        next_section.title
                    )

                    # DO NOT subtract 1.
                    # Multiple sections can share a page.
                    section.end_page = (
                        next_section.start_page
                    )

                # ------------------------------------------
                # Last section of bookmark
                # ------------------------------------------
                else:

                    bookmark = bookmark_lookup[
                        bookmark_title
                    ]

                    section.end_page = (
                        bookmark.end_page
                    )

                    current_index = bookmark_titles.index(
                        bookmark_title
                    )

                    if current_index < len(bookmark_titles) - 1:

                        section.next_bookmark_title = (
                            bookmark_titles[
                                current_index + 1
                            ]
                        )

        logger.info(
            "Extracted %s sections.",
            len(sections),
        )

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
        """
        Extract text starting from the current section title
        and ending just before the next section title.
        """

        # -----------------------------
        # Find current section header
        # -----------------------------
        start_pattern = (
            rf"(?im)^\s*{re.escape(current_title)}\s*$"
        )

        start_match = re.search(start_pattern, text)

        if not start_match:
            return ""

        text = text[start_match.start():]

        # -----------------------------
        # Find next section header
        # -----------------------------
        if next_title:

            end_pattern = (
                rf"(?im)^\s*{re.escape(next_title)}\s*$"
            )

            end_match = re.search(end_pattern, text)

            if end_match:
                text = text[:end_match.start()]

        return text.strip()


    def clean_pdf_noise(self, text: str) -> str:
        lines = text.split("\n")
        out = []

        for l in lines:
            s = l.strip()

            # remove figure captions
            if re.match(r"^Figure\s+\d+", s):
                continue

            # remove diagram artifacts
            if re.fullmatch(r"[SN\s]{3,}", s):
                continue

            # remove footer-like lines
            if re.match(r"^[A-Za-z]+\s+\d+$", s):
                continue

            out.append(s)

        return "\n".join(out).strip()

    def extract_text(
        self,
        reader: PdfReader,
        sections: list[SectionDTO]
    ) -> list[ContentBlockDTO]:

        texts: list[ContentBlockDTO] = []

        total_pages = len(reader.pages)

        sections = sorted(sections, key=lambda s: s.start_page)

        order = 0
        
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

            # NEW STEP (safe place for cleanup section.title)
            clean_text = clean_text.replace(section.title, "", 1).strip()

            texts.append(
                ContentBlockDTO(
                    bookmark_title=section.bookmark_title,
                    section_title=section.title,
                    type="text",
                    order=order,
                    content=clean_text,
                )
            )

            order += 1

        return texts
    
    def extract_images(
        self,
        file: UploadFile,
        sections: list[SectionDTO],
    ) -> list[ImageDTO]:

        images: list[ImageDTO] = []

        file.file.seek(0) 

        pdf = fitz.open(stream=file.file.read(), filetype="pdf")

        print("PyMuPDF pages:", pdf.page_count)

        for section in sections:
            print(
                section.title,
                section.start_page,
                section.end_page,
            )

        os.makedirs("extracted_pages", exist_ok=True)

        for section in sections:

            for page_number in range(
                section.start_page,
                section.end_page + 1,
            ):

                page = pdf.load_page(page_number - 1)

                pix = page.get_pixmap(dpi=300)

                image_path = (
                    f"extracted_pages/"
                    f"{section.bookmark_title}_"
                    f"{section.title}_"
                    f"{page_number}.png"
                )

                image_path = (
                    image_path
                    .replace(" ", "_")
                    .replace("/", "-")
                )

                pix.save(image_path)

                images.append(
                    ImageDTO(
                        bookmark_title=section.bookmark_title,
                        section_title=section.title,
                        page_number=page_number,
                        image_path=image_path,
                    )
                )

        pdf.close()

        return images
    
    def persist_to_database(self):
        return ""