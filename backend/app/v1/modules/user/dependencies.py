from sqlmodel.ext.asyncio.session import AsyncSession

from app.repositories.user_repository import UserRepository

from app.v1.modules.user.services.user_impl_service import (
    UserImplService,
)
from app.v1.modules.user.services.user_service import (
    UserService,
)


# ============================================================
# USER SERVICE
# ============================================================

def get_user_service(
    session: AsyncSession,
) -> UserService:
    """
    Creates the UserService using the provided database session.

    The UserService does not know where the session comes from.

    The caller is responsible for providing the session.

    This keeps the user module independent from:

    - FastAPI dependency injection
    - the application container
    - database session factories
    - request lifecycle management

    The provided session is passed directly to the repository.
    """

    # --------------------------------------------------------
    # CREATE USER REPOSITORY
    # --------------------------------------------------------

    # The repository uses the exact session provided by the caller.

    user_repository = UserRepository(
        session=session,
    )

    # --------------------------------------------------------
    # CREATE USER SERVICE
    # --------------------------------------------------------

    return UserImplService(
        user_repository=user_repository,
    )