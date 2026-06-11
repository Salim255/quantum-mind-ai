from typing import List, Literal
from pydantic import BaseModel
import fitz  # PyMuPDF
import logging
from app.v1.modules.learn.service.doc_ingestion_service_v2 import DocIngestionServiceV2
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

class DocIngestionImplServiceV2(DocIngestionServiceV2):

    # -------------------------
    # MAIN PIPELINE
    # -------------------------
    def pdf_ingestion_pipeline(self, file) -> list[ContentBlockDTO]:

        pdf_bytes = file.file.read()
        pdf = fitz.open(stream=pdf_bytes, filetype="pdf")

        sections = self.extract_sections(pdf)
        #text_blocks = self.extract_text_blocks(pdf, sections)
        #visual_blocks = self.extract_visual_blocks(pdf, sections)

        # return self.merge_content_blocks(text_blocks, visual_blocks)

        return sections
    # =========================================================
    # 1. SECTION EXTRACTION (simple + safe fallback)
    # =========================================================
    def extract_sections(self, pdf: fitz.Document) -> List[SectionDTO]:

        outline = pdf.get_toc(simple=True)
        sections: List[SectionDTO] = []

        for item in outline:
            level, title, page = item

            if level == 1:  # main sections only
                sections.append(
                    SectionDTO(
                        bookmark_title="root",
                        title=title,
                        start_page=page,
                        end_page=0,  # fixed later
                    )
                )

        # compute end pages
        for i in range(len(sections)):
            if i < len(sections) - 1:
                sections[i].end_page = sections[i + 1].start_page - 1
            else:
                sections[i].end_page = len(pdf)

        return sections


    # =========================================================
    # 2. TEXT BLOCKS (ORDER PRESERVED)
    # =========================================================
    def extract_text_blocks(
        self,
        pdf: fitz.Document,
        sections: List[SectionDTO],
    ) -> List[ContentBlockDTO]:

        blocks: List[ContentBlockDTO] = []
        order = 0

        for section in sections:

            for page_num in range(section.start_page, section.end_page + 1):

                page = pdf.load_page(page_num - 1)

                data = page.get_text("blocks")  # IMPORTANT

                # sort by visual order (top → bottom)
                data.sort(key=lambda b: (b[1], b[0]))

                for b in data:

                    x0, y0, x1, y1, text, block_no, block_type = b

                    if not text.strip():
                        continue

                    # skip headers that repeat section title
                    if section.title.lower() in text.lower().strip():
                        continue

                    blocks.append(
                        ContentBlockDTO(
                            bookmark_title=section.bookmark_title,
                            section_title=section.title,
                            type="text",
                            order=order,
                            content=text.strip(),
                        )
                    )

                    order += 1

        return blocks


    # =========================================================
    # 3. VISUAL BLOCKS (PAGE RENDERING)
    # =========================================================
    def extract_visual_blocks(
        self,
        pdf: fitz.Document,
        sections: List[SectionDTO],
    ) -> List[ContentBlockDTO]:

        blocks: List[ContentBlockDTO] = []
        order = 10_000  # ensure visuals come AFTER text in default ordering

        for section in sections:

            image_paths = []

            for page_num in range(section.start_page, section.end_page + 1):

                page = pdf.load_page(page_num - 1)

                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # HD render

                path = f"page_{section.title}_{page_num}.png"
                pix.save(path)

                image_paths.append(path)

            blocks.append(
                ContentBlockDTO(
                    bookmark_title=section.bookmark_title,
                    section_title=section.title,
                    type="visual",
                    order=order,
                    image_path=image_paths,
                )
            )

            order += 1

        return blocks


    # =========================================================
    # 4. MERGE FINAL OUTPUT
    # =========================================================
    def merge_content_blocks(
        self,
        text_blocks: List[ContentBlockDTO],
        visual_blocks: List[ContentBlockDTO],
    ) -> List[ContentBlockDTO]:

        return sorted(
            text_blocks + visual_blocks,
            key=lambda b: b.order,
        )