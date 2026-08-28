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

    - user creation
    - user retrieval
    - user existence checks
    - user-related business rules

    Authentication and security workflows intentionally remain
    outside this service and are handled by AuthService.

    Controllers should depend on this abstraction rather than on
    UserImplService directly.
    """


    # ============================================================
    # CREATE USER
    # ============================================================

    @abstractmethod
    async def create_user(
        self,
        email: str,
        first_name: str,
        last_name: str,
    ) -> UserDTO:
        """
        Creates a new user.

        The implementation is responsible for:

        - creating the user entity
        - applying user-related business rules
        - persisting the user through the repository
        - returning the created user representation

        Authentication credentials and security-related information
        must not be exposed through the returned DTO.
        """

        raise NotImplementedError
    
    # ============================================================
    # GET USER BY ID
    # ============================================================

    @abstractmethod
    async def get_user_by_id(
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

    # ============================================================
    # GET USER BY EMAIL
    # ============================================================

    @abstractmethod
    async def get_user_by_email(
        self,
        email: str,
    ) -> UserDTO | None:
        """
        Retrieves a user by their email address.

        This method is primarily used internally by application
        workflows that need to determine whether an account exists.

        The implementation is responsible for:

        - locating the user associated with the email address
        - returning None when no matching user exists
        - returning the user representation when a match is found

        The absence of a user is not treated as an exception because
        callers may legitimately use this method for existence checks,
        registration workflows and authentication workflows.
        """

        raise NotImplementedError