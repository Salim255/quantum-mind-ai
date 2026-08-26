from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class CookieConfiguration:
    """
    Immutable configuration describing an authentication cookie.

    This object contains HTTP cookie policy but does not depend on
    FastAPI's Response object.
    """

    key: str
    value: str

    httponly: bool
    secure: bool
    samesite: str

    path: str

    max_age: int | None = None
    domain: str | None = None


class CookieConfigurationService(ABC):
    """
    Defines the application's authentication-cookie policy.

    This service centralizes cookie security configuration so that
    authentication code does not repeatedly define:

    - HttpOnly
    - Secure
    - SameSite
    - Path
    - Max-Age
    - Domain

    The service does not directly manipulate FastAPI Response
    objects. The HTTP controller remains responsible for applying
    the returned configuration.
    """

    # ============================================================
    # ACCESS TOKEN COOKIE
    # ============================================================

    @abstractmethod
    def create_access_token_cookie(
        self,
        token: str,
    ) -> CookieConfiguration:
        """
        Creates the configuration for the access-token cookie.
        """

        raise NotImplementedError

    # ============================================================
    # REFRESH TOKEN COOKIE
    # ============================================================

    @abstractmethod
    def create_refresh_token_cookie(
        self,
        token: str,
    ) -> CookieConfiguration:
        """
        Creates the configuration for the refresh-token cookie.
        """

        raise NotImplementedError

    # ============================================================
    # DELETE ACCESS COOKIE
    # ============================================================

    @abstractmethod
    def create_access_token_delete_cookie(
        self,
    ) -> CookieConfiguration:
        """
        Creates the configuration required to remove the
        access-token cookie.
        """

        raise NotImplementedError

    # ============================================================
    # DELETE REFRESH COOKIE
    # ============================================================

    @abstractmethod
    def create_refresh_token_delete_cookie(
        self,
    ) -> CookieConfiguration:
        """
        Creates the configuration required to remove the
        refresh-token cookie.
        """

        raise NotImplementedError

