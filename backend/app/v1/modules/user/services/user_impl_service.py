from uuid import UUID

from app.v1.modules.user.dto.user_dto import UserDTO
from app.repositories.user_repository import UserRepository
from app.v1.modules.user.services.user_service import UserService


class UserImplService(UserService):
    """
    Concrete implementation of the user application service.

    UserImplService implements the use cases defined by UserService
    and coordinates user-related operations with UserRepository.

    This service is responsible for:

    - retrieving users
    - applying user-related business rules
    - converting persistence models into application DTOs
    - propagating application-specific exceptions

    Authentication and security workflows are intentionally not
    handled here. Those responsibilities belong to AuthService.

    Controllers should depend on UserService rather than directly
    depending on this implementation.
    """

    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self._user_repository = user_repository

    # ============================================================
    # GET USER
    # ============================================================

    async def get_user(
        self,
        user_id: UUID,
    ) -> UserDTO | None:
        """
        Retrieves a user by their unique identifier.

        The repository is responsible for locating the user in the
        persistence layer.

        The retrieved persistence model is converted into a UserDTO
        before being returned to the application layer.
        """

        try:
            user = await self._user_repository.get_by_id(
                id=user_id,
            )

            return UserDTO.model_validate(user)

        except Exception:
            raise