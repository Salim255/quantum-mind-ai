from app.models.user_session import UserSession
from app.repositories.base_repository import BaseRepository
from sqlmodel import Session


class UserSessionRepository(
    BaseRepository[UserSession]
):
    """
    Repository for authenticated user session database queries.

    Inherits common CRUD operations from BaseRepository.

    The repository is responsible for data access related to
    individual authenticated sessions.

    Examples of data handled here include:

    - active sessions
    - device information
    - session expiration
    - session revocation
    - last session activity
    - security-version validation

    Refresh-token persistence should be handled by the dedicated
    RefreshTokenRepository rather than mixing token-specific
    queries into this repository.
    """

    def __init__(
        self,
        session: Session,
    ):
        super().__init__(
            session,
            UserSession,
        )

