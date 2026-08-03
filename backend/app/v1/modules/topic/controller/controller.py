
from typing import Annotated
from uuid import UUID

from app.v1.modules.section.dependencies import get_section_service
from app.v1.modules.section.service.section_service import SectionService
from .router import router as topic_router
from fastapi import  Depends, Path, status
from app.v1.modules.topic.service.topic_service import TopicService
from app.v1.modules.block.dto.block_create_dto import BlockCreateDTO
from app.v1.modules.block.service.block_service import BlockService
from app.v1.modules.block.service.block_service import BlockService
from app.v1.modules.block.dto.block_dto import BlockDTO
from app.core.dtos.response_dto import ResponseDTO
from app.v1.modules.topic.dto.topic_create_dto import TopicCreateDTO
from app.v1.modules.topic.dto.topic_update_dto import TopicUpdateDTO
from app.v1.modules.topic.dto.topic_dto import TopicDTO
from app.v1.modules.topic.dependencies import get_topic_service
from app.v1.modules.block.dependencies import get_block_service
from app.v1.modules.section.dto.section_create_dto import SectionCreateDTO
from app.v1.modules.section.dto.section_dto import SectionDTO

# ==========================================================
# CREATE
# ==========================================================
@topic_router.post(
    "/{topic_id}/blocks",
    response_model=ResponseDTO[BlockDTO],
    status_code=status.HTTP_201_CREATED,
    summary="Create a topic block",
    description="""
Create a new learning block attached directly to a Topic.

Topic blocks are introductory pieces of content displayed before the
learner enters the topic's sections.

Typical use cases include:

- Topic introductions
- Learning objectives
- Chapter overviews
- Historical context
- Important notes

The `topic_id` is provided through the URL.

The request body contains the block information only.
""",
    response_description="The newly created topic block.",
)
async def create_topic_block(
    topic_id: Annotated[
        UUID,
        Path(
            description="Identifier of the parent topic."
        ),
    ],
    payload: BlockCreateDTO,
    block_service: Annotated[
        BlockService,
        Depends(get_block_service),
    ],
):

    payload.topic_id = topic_id
    payload.section_id = None

    return ResponseDTO.success(
        await block_service.create_block(payload)
    )

@topic_router.post(
    "/{topic_id}/sections",
    response_model=ResponseDTO[SectionDTO],
    status_code=status.HTTP_201_CREATED,
    summary="Create a topic section",
    description="""
Create a new learning section attached directly to a Topic.
Sections are top-level containers for blocks and represent the main
chapters of a learning topic.
The `topic_id` is provided through the URL.
The request body contains the section information only.
""",
    response_description="The newly created topic section.",
)
async def create_topic_section(
    topic_id: Annotated[
        UUID,
        Path(
            description="Identifier of the parent topic."
        ),
    ],
    payload: SectionCreateDTO,
    section_service: Annotated[
        SectionService,
        Depends(get_section_service),
    ],
) -> ResponseDTO[SectionDTO]:

    payload.topic_id = topic_id

    return ResponseDTO.success(
        await section_service.create_section(payload)
    )


@topic_router.post(
    "/",
    response_model=ResponseDTO[TopicDTO],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new learning topic",
    description="""
Creates a new QuantumMind learning topic.

A topic represents a top-level educational resource.
Sections and blocks are created separately after the topic exists.

Example:

- Topic: Quantum Entanglement
- Category: Quantum Physics
- Slug: quantum-entanglement
""",
    responses={
        201: {
            "description": "Topic successfully created."
        },
        400: {
            "description": "Invalid topic data."
        },
        409: {
            "description": "A topic with this slug already exists."
        },
    },
)
async def create_topic(
    payload: TopicCreateDTO,
    get_topic_service: Annotated[
        TopicService,
        Depends(get_topic_service)
    ]
):  
    return ResponseDTO.success(await get_topic_service.create_topic(payload))
  

# ==========================================================
# GET ONE TOPIC
# ==========================================================

@topic_router.get(
    "/{topic_id}",
    response_model=TopicDTO,
    status_code=status.HTTP_200_OK,
    summary="Get a learning topic",
    description="""
Retrieves a single learning topic.

This endpoint returns only topic information.
It does not include sections or blocks.
""",
    responses={
        200: {
            "description": "Topic retrieved successfully."
        },
        404: {
            "description": "Topic not found."
        },
    },
)
async def get_topic(
    topic_id: str,
    get_topic_service: Annotated[
        TopicService,
        Depends(get_topic_service)
    ]
):
    topic = get_topic_service.get_topic(topic_id)
    return topic



# ==========================================================
# GET TOPIC WITH SECTIONS
# ==========================================================

@topic_router.get(
    "/{topic_id}/sections",
    status_code=status.HTTP_200_OK,
    summary="Get topic with sections",
    description="""
Retrieves a topic together with its learning sections.

Structure:

Topic
 └── Sections

Blocks are not included.
Use this endpoint for navigation and section browsing.
""",
    responses={
        200: {
            "description": "Topic and sections retrieved successfully."
        },
        404: {
            "description": "Topic not found."
        },
    },
)
async def get_topic_with_sections(
    topic_id: str,
    get_topic_service: Annotated[
        TopicService,
        Depends(get_topic_service)
    ]
):
    topic = get_topic_service.get_topic_with_sections(topic_id)
    return topic



# ==========================================================
# GET COMPLETE TOPIC
# ==========================================================

@topic_router.get(
    "/{topic_id}/content",
    status_code=status.HTTP_200_OK,
    summary="Get complete topic content",
    description="""
Retrieves the complete learning hierarchy.

Structure:

Topic
 └── Sections
       └── Blocks


Blocks can represent:

- paragraphs
- equations
- images
- lists
- code examples
- interactive elements

Used for rendering complete learning pages.
""",
    responses={
        200: {
            "description": "Complete learning content retrieved."
        },
        404: {
            "description": "Topic not found."
        },
    },
)
async def get_topic_with_sections_and_blocks(
    topic_id: str,
    get_topic_service: Annotated[
        TopicService,
        Depends(get_topic_service)
    ]
):
    topic = get_topic_service.get_topic_with_sections_and_blocks(topic_id)
    return topic



# ==========================================================
# LIST TOPICS
# ==========================================================
#     response_model=list[TopicDTO],
@topic_router.get(
    "/",

    status_code=status.HTTP_200_OK,
    summary="List learning topics",
    description="""
Returns all available QuantumMind learning topics.

Used for:

- Learn page
- Topic catalogue
- Search results
""",
)
async def get_topics():
    return {"message": "List of all topics."}



# ==========================================================
# UPDATE
# ==========================================================

@topic_router.patch(
    "/{topic_id}",
    response_model=TopicDTO,
    status_code=status.HTTP_200_OK,
    summary="Update a learning topic",
    description="""
Partially updates an existing topic.

Only provided fields are modified.
""",
    responses={
        200: {
            "description": "Topic updated successfully."
        },
        404: {
            "description": "Topic not found."
        },
    },
)
async def update_topic(
    topic_id: str,
    payload: TopicUpdateDTO,
):
    return {"message": "Topic updated successfully."}



# ==========================================================
# DELETE
# ==========================================================

@topic_router.delete(
    "/{topic_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a learning topic",
    description="""
Deletes a topic.

Depending on business rules, related:

- sections
- blocks

may also be removed.
""",
    responses={
        204: {
            "description": "Topic deleted successfully."
        },
        404: {
            "description": "Topic not found."
        },
    },
)
async def delete_topic(
    topic_id: str,
):
    return {"message": "Topic deleted successfully."}