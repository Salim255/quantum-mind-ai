from abc import ABC, abstractmethod
from app.v1.modules.topic.dto.topic_create_dto import TopicCreateDTO
from app.v1.modules.topic.dto.topic_update_dto import TopicUpdateDTO
from app.v1.modules.topic.dto.topic_dto import TopicDTO
from sqlmodel import UUID

class TopicService(ABC):
    """
    Defines the contract for Topic business operations.

    A Topic represents a top-level learning resource
    inside QuantumMind.

    Responsibilities:

        - Create learning topics
        - Retrieve topics
        - Update topic information
        - Remove topics
        - Load topic learning hierarchy

    The service does not handle:
        - database queries
        - SQL operations
        - HTTP concerns

    Those responsibilities belong to:
        Repository layer
        Controller/API layer
    """


    # ==========================================================
    # CREATE
    # ==========================================================
    @abstractmethod
    async def create_topic(
        self,
        topic_data: TopicCreateDTO,
    )-> TopicDTO:
        """
        Creates a new learning topic.

        Example:

            Linear Algebra
            Quantum Entanglement
            Quantum Gates

        Returns:
            The created Topic entity.
        """

        raise NotImplementedError(
            "create_topic() must be implemented"
        )

    # ==========================================================
    # READ
    # ==========================================================
    @abstractmethod
    async def get_topic(
        self,
        topic_id: UUID,
    ):
        """
        Retrieves a single topic by its identifier.

        Does not load sections or blocks.

        Use when only topic metadata is required.
        
        Returns:
            Topic entity.
        """

        raise NotImplementedError(
            "get_topic() must be implemented"
        )



    @abstractmethod
    async def get_topics(self):
        """
        Retrieves all available learning topics.

        Used for:
            - Learn page
            - Topic catalog
            - Search results

        Returns:
            List of topics.
        """

        raise NotImplementedError(
            "get_topics() must be implemented"
        )



    @abstractmethod
    async def get_topic_with_sections(
        self,
        topic_id: UUID,
    ):
        """
        Retrieves a topic together with its sections.

        Example:

            Topic:
                Vectors

            Sections:
                - Introduction
                - Row vectors
                - Column vectors

        Blocks are not loaded.

        Returns:
            Topic with sections.
        """

        raise NotImplementedError(
            "get_topic_with_sections() must be implemented"
        )



    @abstractmethod
    async def get_topic_with_sections_and_blocks(
        self,
        topic_id: UUID,
    ):
        """
        Retrieves the complete learning structure.

        Loads:

            Topic
                |
                └── Sections
                       |
                       └── Blocks


        Used for:
            - Rendering complete lesson pages
            - Learning navigation
            - Client-side scrolling


        Returns:
            Topic containing sections and blocks.
        """

        raise NotImplementedError(
            "get_topic_with_sections_and_blocks() must be implemented"
        )


     # ==========================================================
    # UPDATE
    # ==========================================================

    @abstractmethod
    async def update_topic(
        self,
        topic_id: UUID,
        topic_data: TopicUpdateDTO,
    ):
        """
        Updates topic information.

        Editable fields may include:

            - title
            - description
            - category

        Returns:
            Updated topic entity.
        """

        raise NotImplementedError(
            "update_topic() must be implemented"
        )

    # ==========================================================
    # DELETE
    # ==========================================================

    @abstractmethod
    async def delete_topic(
        self,
        topic_id: UUID,
    ):
        """
        Deletes a topic.

        Depending on business rules this may also remove:

            Topic
              |
              └── Sections
                     |
                     └── Blocks


        Returns:
            None
        """

        raise NotImplementedError(
            "delete_topic() must be implemented"
        )