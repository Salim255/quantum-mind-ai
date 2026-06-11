from pydantic import BaseModel


class ImageDTO(BaseModel):
    """
    Images extracted from PDF.
    """

    bookmark_title: str
    section_title: str

    page_number: int

    image_index: int

    image_name: str

    image_bytes: bytes