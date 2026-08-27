from abc import ABC, abstractmethod
from uuid import UUID

from app.v1.modules.user.dto.user_dto import UserDTO


class UserService(ABC):
    """
    Defines the application-level user contract.

    UserService is responsible for exposing user-related application
    use cases without coupling controllers to their concrete
    implementation.

    The implementation coordinates:

    - UserRepository
    - user retrieval
    - user existence checks
    - user-related business rules

    Authentication and security workflows intentionally remain
    outside this service and are handled by AuthService.

    Controllers should depend on this abstraction rather than on
    UserImplService directly.
    """

    # ============================================================
    # GET USER
    # ============================================================

    @abstractmethod
    async def get_user(
        self,
        user_id: UUID,
    ) -> UserDTO:
        """
        Retrieves a user by their unique identifier.

        The implementation is responsible for:

        - locating the requested user
        - handling the case where the user does not exist
        - returning the user representation

        Authentication credentials and security-related information
        must not be exposed through the returned DTO.
        """

        raise NotImplementedError