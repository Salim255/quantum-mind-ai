
from .router import router as topic_router
from fastapi import  status
from app.v1.modules.topic.dto.topic_create_dto import TopicCreateDTO
from app.v1.modules.topic.dto.topic_update_dto import TopicUpdateDTO
from app.v1.modules.topic.dto.topic_dto import TopicDTO



# ==========================================================
# CREATE
# ==========================================================

@topic_router.post(
    "/",
    response_model=TopicDTO,
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
):  
    print("Received payload:", payload)  # Debugging line
    return {"message": "Topic created successfully."}



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
):
    return {"message": "Topic retrieved successfully."}



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
):
    return {"message": "Topic and sections retrieved successfully."}



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
):
    return {"message": "Complete topic content retrieved."}



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