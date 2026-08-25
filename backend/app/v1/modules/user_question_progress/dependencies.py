from typing import Annotated

from fastapi import Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.container import Container
from app.repositories.user_question_progress_repository import (
    UserQuestionProgressRepository,
)
from app.v1.modules.user_question_progress.services.user_question_progress_impl_service import (
    UserQuestionProgressImplService,
)
from app.v1.modules.user_question_progress.services.user_question_progress_service import (
    UserQuestionProgressService,
)


# ============================================================
# CONTAINER DEPENDENCY
# ============================================================

def get_container(
    request: Request,
) -> Container:
    """
    Retrieve the application dependency container.
    """

    return request.app.state.container


# ============================================================
# DATABASE SESSION DEPENDENCY
# ============================================================

async def get_db_session(
    container: Annotated[
        Container,
        Depends(get_container),
    ],
):
    """
    Provide an asynchronous database session.
    """

    async for session in container.db_session.get_session():
        yield session


# ============================================================
# REPOSITORY DEPENDENCY
# ============================================================

def get_user_question_progress_repository(
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
) -> UserQuestionProgressRepository:
    """
    Create the UserQuestionProgressRepository for the current request.
    """

    return UserQuestionProgressRepository(session)


# ============================================================
# SERVICE DEPENDENCY
# ============================================================

def get_user_question_progress_service(
    user_question_progress_repository: Annotated[
        UserQuestionProgressRepository,
        Depends(get_user_question_progress_repository),
    ],
) -> UserQuestionProgressService:
    """
    Create the UserQuestionProgressService for the current request.
    """

    return UserQuestionProgressImplService(
        user_question_progress_repository=(
            user_question_progress_repository
        ),
    )