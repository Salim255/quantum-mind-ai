from abc import ABC, abstractmethod
from uuid import UUID
from datetime import datetime

from app.v1.modules.user_session.dto.user_session_dto import (
    UserSessionDTO,
)


class UserSessionService(ABC):
    """
    Defines the application-level user session contract.

    UserSessionService is responsible for managing authenticated
    session state associated with user accounts.

    The service owns session lifecycle operations such as:

    - creating authenticated sessions
    - retrieving sessions
    - validating session state
    - rotating refresh-token state
    - revoking sessions

    The raw refresh token must never be persisted.

    Refresh-token hashing and comparison are security concerns and
    should be handled before persistence.

    JWT creation remains the responsibility of JWTManagerService.

    User account management remains the responsibility of
    UserService.

    Security state management remains the responsibility of
    UserSecurityService.

    Controllers and higher-level application services should depend
    on this abstraction rather than on UserSessionImplService.
    """

    # ============================================================
    # CREATE SESSION
    # ============================================================

    @abstractmethod
    async def create_session(
        self,
        user_id: UUID,
        refresh_token_hash: str,
        security_version: int,
        expires_at: datetime | None,
        device_name: str | None = None,
        user_agent: str | None = None,
        ip_address: str | None = None,
    ) -> UserSessionDTO:
        """
        Creates a new authenticated session.

        The session stores only the cryptographic hash of the
        refresh token.

        The raw refresh token must never be passed to or persisted
        by the repository.

        The session captures the user's current security version so
        that later security-version changes can invalidate the
        session globally.

        Device and client metadata are stored for session management
        and security auditing.
        """

        raise NotImplementedError

    # ============================================================
    # GET SESSION
    # ============================================================

    @abstractmethod
    async def get_session_by_id(
        self,
        session_id: UUID,
    ) -> UserSessionDTO:
        """
        Retrieves an authentication session by its unique identifier.

        This method returns the persisted session state without
        performing authentication itself.
        """

        raise NotImplementedError

    # ============================================================
    # GET SESSION BY REFRESH TOKEN HASH
    # ============================================================

    @abstractmethod
    async def get_session_by_refresh_token_hash(
        self,
        refresh_token_hash: str,
    ) -> UserSessionDTO:
        """
        Retrieves the session associated with a refresh-token hash.

        Only the cryptographic hash of the presented refresh token
        should be used for persistence lookup.

        The raw refresh token must never be persisted.
        """

        raise NotImplementedError

    # ============================================================
    # VALIDATE SESSION
    # ============================================================

    @abstractmethod
    async def validate_session(
        self,
        session: UserSessionDTO,
        security_version: int,
    ) -> bool:
        """
        Determines whether a session is currently valid.

        A session is valid only when:

        - it has not been revoked
        - it has not expired
        - its security version matches the user's current
          security version

        This method evaluates session state only.

        It does not generate tokens or modify authentication
        credentials.
        """

        raise NotImplementedError

    # ============================================================
    # ROTATE REFRESH TOKEN
    # ============================================================

    @abstractmethod
    async def rotate_refresh_token(
        self,
        session: UserSessionDTO,
        refresh_token_hash: str,
    ) -> UserSessionDTO:
        """
        Rotates the refresh-token state associated with a session.

        The current refresh-token hash becomes the previous token
        hash and the newly generated refresh-token hash becomes the
        current token hash.

        The token version is incremented.

        The session's last-used timestamp is updated.

        The raw refresh token must never be persisted.
        """

        raise NotImplementedError

    # ============================================================
    # REVOKE SESSION
    # ============================================================

    @abstractmethod
    async def revoke_session(
        self,
        session_id: UUID,
    ) -> UserSessionDTO:
        """
        Revokes an authenticated session.

        A revoked session must no longer be accepted for refresh.

        Revocation is idempotent: revoking an already revoked
        session should not restore or otherwise reactivate it.
        """

        raise NotImplementedError


    # ============================================================
    # UPDATE REFRESH TOKEN
    # ============================================================

    @abstractmethod
    async def update_refresh_token(
        self,
        session_id: UUID,
        refresh_token_hash: str,
        expires_at: datetime,
    ) -> UserSessionDTO:
        """
        Updates the refresh-token information of an existing session.

        This method is responsible for completing or rotating the
        refresh-token state associated with a session.

        The raw refresh token must never be persisted.

        Only its cryptographic hash is stored.

        The implementation is responsible for updating:

        - the refresh-token hash
        - the refresh-token expiration date

        The session identifier is used to locate the session that
        should be updated.

        Raises an application-specific exception when the session
        cannot be located or updated.
        """

        raise NotImplementedError