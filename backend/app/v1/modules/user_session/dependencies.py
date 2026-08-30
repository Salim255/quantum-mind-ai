from sqlmodel.ext.asyncio.session import AsyncSession

from app.repositories.user_session_repository import (
    UserSessionRepository,
)

from app.v1.modules.user_session.services.user_session_service import (
    UserSessionService,
)

from app.v1.modules.user_session.services.user_session_impl_service import (
    UserSessionImplService,
)


# ============================================================
# USER SESSION SERVICE
# ============================================================

def get_user_session_service(
    session: AsyncSession,
) -> UserSessionService:
    """
    Creates the UserSessionService for the current database session.

    The database session is supplied by the application layer,
    normally through the controller.

    This dependency does NOT:

    - create a database session
    - retrieve the Container
    - use FastAPI Depends()
    - manage the database transaction

    Its responsibility is only to assemble the user-session module:

        AsyncSession
             │
             ▼
        UserSessionRepository
             │
             ▼
        UserSessionImplService
             │
             ▼
        UserSessionService


    The supplied AsyncSession can be the same session used by
    the other services participating in the same operation.
    """

    # --------------------------------------------------------
    # CREATE USER SESSION REPOSITORY
    # --------------------------------------------------------

    # The repository receives the session supplied by the
    # application layer.
    user_session_repository = UserSessionRepository(
        session=session,
    )

    # --------------------------------------------------------
    # CREATE USER SESSION SERVICE
    # --------------------------------------------------------

    # The service receives the repository.
    #
    # The service does not know where the session came from.
    # It only works with its repository abstraction.
    return UserSessionImplService(
        user_session_repository=user_session_repository,
    )