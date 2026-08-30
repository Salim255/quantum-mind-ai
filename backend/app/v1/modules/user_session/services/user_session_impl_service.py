import logging
from datetime import UTC, datetime
from uuid import UUID

from app.core.exceptions.base_exception import AppException
from app.core.exceptions.custom_exceptions import ProcessingException

from app.v1.modules.user_session.dto.user_session_dto import UserSessionDTO

from app.models.user_session import UserSession

from app.repositories.user_session_repository import UserSessionRepository

from app.v1.modules.user_session.services.user_session_service import (UserSessionService)


logger = logging.getLogger(__name__)


class UserSessionImplService(UserSessionService):
    """
    Concrete implementation of the user session service.

    UserSessionImplService manages the lifecycle of authenticated
    user sessions.

    Its responsibility is limited to session-state management.

    It coordinates:

    - UserSessionRepository
    - session creation
    - session retrieval
    - session expiration checks
    - security-version validation
    - refresh-token rotation
    - session revocation
    - session usage auditing

    It does not manage:

    - User creation or retrieval
    - password hashing or verification
    - JWT creation
    - authentication cookies
    - user security state
    - profile information

    Higher-level authentication workflows are orchestrated by
    AuthImplService.

    Unexpected implementation or infrastructure errors are logged
    internally and converted into the shared ProcessingException.
    """

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(
        self,
        user_session_repository: UserSessionRepository,
    ) -> None:
        """
        Initializes the user session service.

        UserSessionRepository:
            Provides persistence operations for UserSession records.
        """

        self.user_session_repository = (
            user_session_repository
        )

    # ============================================================
    # CREATE SESSION
    # ============================================================

    async def create_session(
        self,
        user_id: UUID,
        refresh_token_hash: str | None,
        security_version: int,
        expires_at: datetime | None,
        device_name: str | None = None,
        user_agent: str | None = None,
        ip_address: str | None = None,
    ) -> UserSessionDTO:
        """
        Creates a new authenticated session.

        Only the refresh-token hash is persisted.

        The raw refresh token must never reach the persistence layer.
        """

        try:

            # ----------------------------------------------------
            # CREATE SESSION
            # ----------------------------------------------------

            session = UserSession(
                user_id=user_id,
                refresh_token_hash=refresh_token_hash,
                security_version=security_version,
                expires_at=expires_at,
                device_name=device_name,
                user_agent=user_agent,
                ip_address=ip_address,
                last_ip_address=ip_address,
            )

            # ----------------------------------------------------
            # PERSIST SESSION
            # ----------------------------------------------------

            session = await self.user_session_repository.add(session)

            # ----------------------------------------------------
            # RETURN SESSION DTO
            # ----------------------------------------------------

            return UserSessionDTO.model_validate(
                session
            )

        except AppException:
            raise

        except Exception as exception:
            logger.exception(
                "Error in creating user session"
            )

            raise ProcessingException(
                message="Unable to create user session.",
            ) from exception

    # ============================================================
    # GET SESSION
    # ============================================================

    async def get_session_by_id(
        self,
        session_id: UUID,
    ) -> UserSessionDTO:
        """
        Retrieves an authentication session by its identifier.
        """

        try:

            # ----------------------------------------------------
            # RETRIEVE SESSION
            # ----------------------------------------------------

            session = await (
                self.user_session_repository.get_by_id(
                    session_id
                )
            )

            if session is None:
                raise ProcessingException(
                    message="Unable to retrieve user session.",
                )

            # ----------------------------------------------------
            # RETURN SESSION DTO
            # ----------------------------------------------------

            return UserSessionDTO.model_validate(
                session
            )

        except AppException:
            raise

        except Exception as exception:
            logger.exception(
                "Error in getting user session by id"
            )

            raise ProcessingException(
                message="Unable to retrieve user session.",
            ) from exception

    # ============================================================
    # GET SESSION BY REFRESH TOKEN HASH
    # ============================================================

    async def get_session_by_refresh_token_hash(
        self,
        refresh_token_hash: str,
    ) -> UserSessionDTO:
        """
        Retrieves a session using the hash of its current
        refresh token.

        The raw refresh token is never persisted or used as a
        database lookup value.
        """

        try:

            # ----------------------------------------------------
            # RETRIEVE SESSION
            # ----------------------------------------------------

            session = await (
                self.user_session_repository
                .get_by_refresh_token_hash(
                    refresh_token_hash
                )
            )

            if session is None:
                raise ProcessingException(
                    message="Unable to retrieve user session.",
                )

            # ----------------------------------------------------
            # RETURN SESSION DTO
            # ----------------------------------------------------

            return UserSessionDTO.model_validate(
                session
            )

        except AppException:
            raise

        except Exception as exception:
            logger.exception(
                "Error in getting user session by refresh token hash"
            )

            raise ProcessingException(
                message="Unable to retrieve user session.",
            ) from exception

    # ============================================================
    # VALIDATE SESSION
    # ============================================================

    async def validate_session(
        self,
        session: UserSessionDTO,
        security_version: int,
    ) -> bool:
        """
        Determines whether an authentication session is currently
        valid.

        A session is invalid when:

        - it has been revoked
        - it has expired
        - its security version no longer matches the user's
          current security version
        """

        try:

            # ----------------------------------------------------
            # CHECK REVOCATION
            # ----------------------------------------------------

            if session.revoked_at is not None:
                return False

            # ----------------------------------------------------
            # CHECK EXPIRATION
            # ----------------------------------------------------

            now = datetime.now(UTC)

            if session.expires_at <= now:
                return False

            # ----------------------------------------------------
            # CHECK SECURITY VERSION
            # ----------------------------------------------------

            if (
                session.security_version
                != security_version
            ):
                return False

            return True

        except AppException:
            raise

        except Exception as exception:
            logger.exception(
                "Error in validating user session"
            )

            raise ProcessingException(
                message="Unable to validate user session.",
            ) from exception

    # ============================================================
    # ROTATE REFRESH TOKEN
    # ============================================================

    async def rotate_refresh_token(
        self,
        session: UserSessionDTO,
        refresh_token_hash: str,
    ) -> UserSessionDTO:
        """
        Rotates the refresh-token hash associated with a session.

        The existing current hash becomes the previous hash.

        The supplied new hash becomes the current refresh-token
        hash.

        The token version is incremented.

        The operation also records the time at which the session
        was successfully used.
        """

        try:

            # ----------------------------------------------------
            # CURRENT UTC TIME
            # ----------------------------------------------------

            now = datetime.now(UTC)

            # ----------------------------------------------------
            # ROTATE TOKEN STATE
            # ----------------------------------------------------

            update_data = {
                "previous_token_hash": (
                    session.refresh_token_hash
                ),
                "refresh_token_hash": refresh_token_hash,
                "token_version": (
                    session.token_version + 1
                ),
                "last_used_at": now,
                "updated_at": now,
            }

            # ----------------------------------------------------
            # PERSIST ROTATION
            # ----------------------------------------------------

            updated_session = await (
                self.user_session_repository.update(
                    session.id,
                    update_data,
                )
            )

            # ----------------------------------------------------
            # RETURN UPDATED SESSION
            # ----------------------------------------------------

            return UserSessionDTO.model_validate(
                updated_session
            )

        except AppException:
            raise

        except Exception as exception:
            logger.exception(
                "Error in rotating refresh token"
            )

            raise ProcessingException(
                message="Unable to rotate refresh token.",
            ) from exception

    # ============================================================
    # REVOKE SESSION
    # ============================================================

    async def revoke_session(
        self,
        session_id: UUID,
    ) -> UserSessionDTO:
        """
        Revokes an authenticated session.

        Revocation is permanent for the current session and prevents
        further refresh operations.
        """

        try:

            # ----------------------------------------------------
            # CURRENT UTC TIME
            # ----------------------------------------------------

            now = datetime.now(UTC)

            # ----------------------------------------------------
            # REVOKE SESSION
            # ----------------------------------------------------

            updated_session = await (
                self.user_session_repository.update(
                    session_id,
                    {
                        "revoked_at": now,
                        "updated_at": now,
                    },
                )
            )

            # ----------------------------------------------------
            # RETURN UPDATED SESSION
            # ----------------------------------------------------

            return UserSessionDTO.model_validate(
                updated_session
            )

        except AppException:
            raise

        except Exception as exception:
            logger.exception(
                "Error in revoking user session"
            )

            raise ProcessingException(
                message="Unable to revoke user session.",
            ) from exception