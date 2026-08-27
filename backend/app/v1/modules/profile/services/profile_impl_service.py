from uuid import UUID
from app.core.exceptions.profile_exception import (ProfileException)
from app.v1.modules.profile.dto.profile_dto import (ProfileDTO, CreateProfileDTO)
from app.v1.modules.profile.services.profile_service import ProfileService
from app.repositories.profile_repository import ProfileRepository

import logging

logger = logging.getLogger(__name__)

class ProfileImplService(ProfileService):
    """
    Concrete implementation of the profile application service.

    ProfileImplService implements the profile use cases defined by
    ProfileService and coordinates profile-related operations with
    ProfileRepository.

    This service is responsible for:

    - coordinating profile creation
    - coordinating profile retrieval
    - applying profile business rules
    - translating repository results into application DTOs
    - propagating application-specific exceptions

    Controllers should depend on ProfileService rather than directly
    depending on this implementation.
    """

    def __init__(
        self,
        profile_repository: ProfileRepository,
    ):
        self._profile_repository = profile_repository

    # ============================================================
    # CREATE PROFILE
    # ============================================================

    async def create_profile(
        self,
        payload: CreateProfileDTO,
    ) -> ProfileDTO:
        """
        Creates a profile for an existing user.

        The profile repository is responsible for persisting the
        profile data.

        The payload contains:

        - user_id
        - first_name
        - last_name

        The created profile is returned as a ProfileDTO.
        """

        try:
            profile = await self._profile_repository.add(
                payload=payload,
            )

            return ProfileDTO.model_validate(profile)

        except Exception as e:
            logger.exception("Error in create profile")
            raise ProfileException() from e

    # ============================================================
    # GET PROFILE
    # ============================================================

    async def get_profile(
        self,
        user_id: UUID,
    ) -> ProfileDTO:
        """
        Retrieves the profile associated with a user.

        The profile is located using the user's unique identifier.

        If the repository cannot find a profile, the repository or
        application exception handling layer is responsible for
        raising the appropriate exception.
        """

        try:
            profile = await self._profile_repository.get_by_user_id(
                user_id=user_id,
            )

            return ProfileDTO.model_validate(profile)

        except Exception as e:
            logger.exception("Error in get profile")
            raise ProfileException() from e