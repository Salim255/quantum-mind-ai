from pydantic import BaseModel

class ContentBlockDTO(BaseModel):
    type: Literal["text", "figure", "equation", "circuit"]

    order: int

    content: str | None = None

    image_path: str | None = None

    caption: str | None = None
    
class SectionDTO(BaseModel):
    bookmark_title: str

    title: str

    start_page: int

    end_page: int

    next_section_title: str | None = None

    next_bookmark_title: str | None = None
