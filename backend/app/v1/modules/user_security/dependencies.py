from sqlmodel.ext.asyncio.session import AsyncSession

from app.repositories.user_security_repository import (
    UserSecurityRepository,
)

from app.v1.modules.user_security.services.user_security_service import (
    UserSecurityService,
)

from app.v1.modules.user_security.services.user_security_impl_service import (
    UserSecurityImplService,
)


# ============================================================
# USER SECURITY SERVICE
# ============================================================

def get_user_security_service(
    session: AsyncSession,
) -> UserSecurityService:
    """
    Creates the UserSecurityService for the current database session.

    The database session is supplied by the application layer,
    normally through the controller.

    This dependency does NOT create or retrieve a database session.

    Its responsibility is only to assemble the user-security module:

        AsyncSession
             │
             ▼
        UserSecurityRepository
             │
             ▼
        UserSecurityImplService
             │
             ▼
        UserSecurityService


    The same AsyncSession can be shared with other services
    participating in the same application operation.
    """

    # --------------------------------------------------------
    # CREATE USER SECURITY REPOSITORY
    # --------------------------------------------------------

    # The repository receives the session supplied by the
    # application layer.
    user_security_repository = UserSecurityRepository(
        session=session,
    )

    # --------------------------------------------------------
    # CREATE USER SECURITY SERVICE
    # --------------------------------------------------------

    # The service receives the repository and remains unaware
    # of FastAPI, Request, Container, or Depends().
    return UserSecurityImplService(
        user_security_repository=user_security_repository,
    )