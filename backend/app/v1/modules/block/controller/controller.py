from typing import Annotated

from fastapi import Depends, status

from app.core.dtos.response_dto import ResponseDTO
from app.v1.modules.block.dependencies import get_block_service
from app.v1.modules.block.dto.block_dto import BlockDTO
from app.v1.modules.block.dto.block_create_dto import BlockCreateDTO
from app.v1.modules.block.service.block_service import BlockService

from .router import router as block_router


@block_router.post(
    "/",
    response_model=ResponseDTO[BlockDTO],
    status_code=status.HTTP_201_CREATED,
    summary="Create a learning block",
    description="""
Create a new educational block inside QuantumMind.

A block is the smallest unit of educational content.

A block can belong to **either**:

- a Topic (topic introduction)
- a Section (section content)

Exactly one parent must be provided.

Examples of block types include:

- paragraph
- heading
- equation
- image
- example
- exercise
- quote

The created block is returned after it has been successfully persisted.
""",
    response_description="The newly created learning block.",
)
async def create_block(
    payload: BlockCreateDTO,
    block_service: Annotated[
        BlockService,
        Depends(get_block_service),
    ],
) -> ResponseDTO[BlockDTO]:
    """
    Create a new learning block.

    This endpoint is typically used by the content management
    interface to build learning resources.

    Returns:
        The newly created block.
    """
    return ResponseDTO.success(
        await block_service.create_block(payload)
    )