from pydantic import BaseModel


class SectionDTO(BaseModel):
    bookmark_title: str

    title: str

    start_page: int

    end_page: int

    next_section_title: str | None = None

    next_bookmark_title: str | None = None
