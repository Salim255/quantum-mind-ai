# app/v1/modules/learn/dto/equation_dto.py

from pydantic import BaseModel


class EquationDTO(BaseModel):
    """
    Mathematical equations extracted from a section.
    """

    bookmark_title: str

    section_title: str

    latex: str

    page_number: int