from uuid import UUID

import logging

from app.core.exceptions.custom_exceptions import (
    ProcessingException,
)
from app.core.exceptions.error_code import ErrorCode

from app.repositories.user_repository import UserRepository

from app.v1.modules.user.dto.user_dto import UserDTO
from app.v1.modules.user.services.user_service import UserService


logger = logging.getLogger(__name__)


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
    # CREATE USER
    # ============================================================

    async def create_user(
        self,
        email: str,
        first_name: str,
        last_name: str,
    ) -> UserDTO:
        """
        Creates a new user.

        The repository is responsible for persisting the user in the
        database.

        The created persistence model is converted into a UserDTO
        before being returned to the application layer.

        Authentication credentials and security-related information
        must not be handled by this service.
        """

        try:
            user = await self._user_repository.add(
                email=email,
                first_name=first_name,
                last_name=last_name,
            )

            return UserDTO.model_validate(user)

        except Exception as exception:
            logger.exception("Error creating user")

            raise ProcessingException(
                message="Unable to create the user.",
                error_code=ErrorCode.USER_PROCESSING_ERROR,
            ) from exception
        
    # ============================================================
    # GET USER BY ID
    # ============================================================

    async def get_user_by_id(
        self,
        user_id: UUID,
    ) -> UserDTO | None:
        """
        Retrieves a user by their unique identifier.

        The repository is responsible for locating the user in the
        persistence layer.

        The retrieved persistence model is converted into a UserDTO
        before being returned to the application layer.

        Returns None when no user exists with the provided
        identifier.
        """

        try:
            user = await self._user_repository.get_by_id(
                id=user_id,
            )

            if user is None:
                return None

            return UserDTO.model_validate(user)

        except Exception as exception:
            logger.exception("Error getting user by ID")

            raise ProcessingException(
                message="Unable to retrieve the user.",
                error_code=ErrorCode.USER_PROCESSING_ERROR,
            ) from exception

    # ============================================================
    # GET USER BY EMAIL
    # ============================================================

    async def get_user_by_email(
        self,
        email: str,
    ) -> UserDTO | None:
        """
        Retrieves a user by their email address.

        The repository is responsible for locating the user in the
        persistence layer.

        The retrieved persistence model is converted into a UserDTO
        before being returned to the application layer.

        Returns None when no user exists with the provided
        email address.
        """

        try:
            user = await self._user_repository.get_by_email(
                email=email,
            )

            if user is None:
                return None

            return UserDTO.model_validate(user)

        except Exception as exception:
            logger.exception("Error getting user by email")

            raise ProcessingException(
                message="Unable to retrieve the user.",
                error_code=ErrorCode.USER_PROCESSING_ERROR,
            ) from exception