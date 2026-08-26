from app.models.user_security import UserSecurity
from app.repositories.base_repository import BaseRepository
from sqlmodel import Session


class UserSecurityRepository(
    BaseRepository[UserSecurity]
):
    """
    Repository for user security database queries.

    Inherits common CRUD operations from BaseRepository.

    The repository is responsible for data access related to
    authentication and security state belonging to a user.

    Examples of data handled here include:

    - email verification state
    - failed login attempts
    - account lock state
    - password security metadata
    - security version
    - authentication-related security state
    """

    def __init__(
        self,
        session: Session,
    ):
        super().__init__(
            session,
            UserSecurity,
        )

