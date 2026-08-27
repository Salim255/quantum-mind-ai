from abc import ABC, abstractmethod

from app.v1.modules.profile.dto.profile_dto import ProfileDTO


class ProfileService(ABC):
    """
    Defines the application-level profile contract.

    ProfileService is responsible for exposing profile-related
    application use cases without coupling controllers to their
    concrete implementation.

    The implementation coordinates:

    - ProfileRepository
    - profile validation rules
    - profile creation rules
    - profile retrieval rules

    Controllers should depend on this abstraction rather than on
    ProfileImplService directly.
    """

    # ============================================================
    # CREATE PROFILE
    # ============================================================

    @abstractmethod
    async def create_profile(
        self,
        user_id: str,
        payload: ProfileDTO,
    ) -> ProfileDTO:
        """
        Creates a profile for an existing user.

        The profile creation workflow is responsible for:

        - validating the profile payload
        - associating the profile with the user
        - ensuring the profile can only be created for a valid user
        - persisting the profile
        - returning the created profile

        Profile creation should respect the application's profile
        business rules and must not allow invalid or inconsistent
        profile state to be persisted.
        """

        raise NotImplementedError

    # ============================================================
    # GET PROFILE
    # ============================================================

    @abstractmethod
    async def get_profile(
        self,
        user_id: str,
    ) -> ProfileDTO:
        """
        Retrieves the profile associated with a user.

        The implementation is responsible for:

        - locating the profile using the user identifier
        - handling the case where the profile does not exist
        - returning the profile data

        The controller should not access the repository directly.
        Profile retrieval and its associated business rules belong
        to the service layer.
        """

        raise NotImplementedError