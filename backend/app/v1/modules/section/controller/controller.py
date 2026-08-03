from app.core.dtos.response_dto import ResponseDTO
from app.v1.modules.block.dto.block_create_dto import BlockCreateDTO
from app.v1.modules.block.service.block_service import BlockService
from app.v1.modules.block.dependencies import get_block_service
from app.v1.modules.block.dependencies import get_block_service
from fastapi import Depends, Path, status
from uuid import UUID
from typing import Annotated
from .router import router as section_router

@section_router.post(
    "/{section_id}/blocks",
    status_code=status.HTTP_201_CREATED,
    summary="Create a section block",
    description="""
Create a new learning block attached directly to a Section.
Blocks are the smallest units of learning content and can be of various 
types (e.g., text, video, quiz, etc.). They are contained within sections,
which in turn belong to topics."""
)
async def create_section_block(
    section_id: Annotated[
        UUID,
        Path(
            description="Identifier of the parent section."
        ),
    ],
    payload: BlockCreateDTO,
    block_service: Annotated[
        BlockService,
        Depends(get_block_service),
    ],
):

    payload.section_id = section_id
    payload.topic_id = None

    return ResponseDTO.success(
        await block_service.create_block(payload)
    )   
