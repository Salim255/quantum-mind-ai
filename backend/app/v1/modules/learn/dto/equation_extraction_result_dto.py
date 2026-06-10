from pydantic import BaseModel

from app.v1.modules.learn.dto.equation_dto import EquationDTO


class EquationExtractionResultDTO(BaseModel):
    equations: list[EquationDTO]