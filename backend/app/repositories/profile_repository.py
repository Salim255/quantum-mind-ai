from app.models.profile import Profile
from app.repositories.base_repository import BaseRepository
from sqlmodel import Session


class ProfileRepository(
    BaseRepository[Profile]
):
    """
    Repository for user profile database queries.

    Inherits common CRUD operations from BaseRepository.

    The repository is responsible for data access related to
    user personal, presentation, and learning-profile information.

    Examples of data handled here include:

    - first name
    - last name
    - display name
    - avatar
    - biography
    - learning preferences
    - learning level
    """

    def __init__(
        self,
        session: Session,
    ):
        super().__init__(
            session,
            Profile,
        )

