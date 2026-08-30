from sqlmodel.ext.asyncio.session import AsyncSession

from app.repositories.profile_repository import (
    ProfileRepository,
)

from app.v1.modules.profile.services.profile_service import (
    ProfileService,
)

from app.v1.modules.profile.services.profile_impl_service import (
    ProfileImplService,
)


# ============================================================
# PROFILE SERVICE
# ============================================================

def get_profile_service(
    session: AsyncSession,
) -> ProfileService:
    """
    Creates the ProfileService for the current database session.

    The database session is supplied by the application layer
    (normally the controller).

    This dependency does not create or retrieve the session.

    Its only responsibility is to assemble the profile module:

        AsyncSession
             │
             ▼
        ProfileRepository
             │
             ▼
        ProfileImplService
             │
             ▼
        ProfileService


    IMPORTANT:

    The same AsyncSession can be passed to multiple services.

    For example, during user registration:

        Controller
            │
            │ session
            ├──────────────────────┐
            │                      │
            ▼                      ▼
        UserService          ProfileService
            │                      │
            ▼                      ▼
        UserRepository       ProfileRepository
            │                      │
            └──────────┬───────────┘
                       │
                       ▼
                 Same AsyncSession

    This allows all database operations belonging to the
    same application transaction to participate in the
    same SQLAlchemy session.
    """

    # --------------------------------------------------------
    # CREATE PROFILE REPOSITORY
    # --------------------------------------------------------

    # The repository receives the session supplied by the
    # application layer.
    profile_repository = ProfileRepository(
        session=session,
    )

    # --------------------------------------------------------
    # CREATE PROFILE SERVICE
    # --------------------------------------------------------

    # The service receives the repository and remains unaware
    # of FastAPI, Request, Container, or dependency injection.
    return ProfileImplService(
        profile_repository=profile_repository,
    )