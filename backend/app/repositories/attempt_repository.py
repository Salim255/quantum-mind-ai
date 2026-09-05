from app.repositories.base_repository import BaseRepository
from app.models.attempt import Attempt
from app.models.question import Question
from app.models.topic import Topic
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select
from uuid import UUID


class AttemptRepository(BaseRepository[Attempt]):
    """
    Repository for quiz_attempts database queries.

    Inherits common CRUD operations from BaseRepository.
    """
     
    def __init__(self, session: Session):
        super().__init__(session, Attempt)


           
    async def get_by_id_with_topic(
        self,
        attempt_id: UUID,
    ) -> Attempt | None:
        """
        Retrieve an attempt together with its associated topic.

        This method explicitly loads the topic to prevent lazy-loading
        database operations during asynchronous DTO serialization.

        Args:
            attempt_id:
                Identifier of the attempt.

        Returns:
            The attempt with its topic loaded, or None if not found.
        """
        statement = (
                select(Attempt)
                .options(
                    selectinload(Attempt.topic),
                )
                .where(
                    Attempt.id == attempt_id,
                )
            )

        result = await self.session.execute(statement)

        result = result.scalar_one_or_none()
        
        if result:
            print("Attempt ID:✅✅", result.id)
            print("Topic ID: 💥💥", result.topic_id)
            print("Loaded topic: 🛑🛑", result.topic)
        return result
    
    # ============================================================
    # ATTEMPT + TOPIC + QUESTIONS + ANSWERS
    # ============================================================

    async def get_by_id_with_topic_questions(
        self,
        attempt_id: UUID,
    ) -> Attempt | None:
        """
        Retrieve an attempt with its complete learning content.

        The returned object contains:

            Attempt
                └── Topic
                     └── Questions
                          └── Answers

        Questions are loaded through the attempt's topic and their
        answer options are loaded together with each question.

        This query is intended for starting or resuming a quiz,
        where the client needs all questions and their available
        answer options.

        Args:
            attempt_id:
                Identifier of the attempt.

        Returns:
            The attempt with topic, questions, and answers loaded,
            or None if the attempt does not exist.
        """
        statement = (
            select(Attempt)
            .options(
                selectinload(
                    Attempt.topic
                )
                .selectinload(
                    Topic.questions
                )
                .selectinload(
                    Question.answers
                ),
            )
            .where(
                Attempt.id == attempt_id,
            )
        )

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()


    # ============================================================
    # LATEST ATTEMPT BY USER / TOPIC
    # ============================================================

    async def get_latest_attempt_by_user_and_topic(
        self,
        user_id: UUID,
        topic_id: UUID,
    ) -> Attempt | None:
        """
        Retrieve the latest attempt made by a user for a specific topic.

        The user_id and topic_id are both required.

        If the user has never attempted the specified topic,
        None is returned.

        Args:
            user_id:
                Identifier of the user.

            topic_id:
                Identifier of the topic.

        Returns:
            The user's latest attempt for the topic,
            or None if no attempt exists.
        """

        statement = (
            select(Attempt)
            .where(
                Attempt.user_id == user_id,
                Attempt.topic_id == topic_id,
            )
            .order_by(
                Attempt.started_at.desc(),
            )
            .limit(1)
        )

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()