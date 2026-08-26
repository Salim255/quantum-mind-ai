from fastapi import Response

from app.core.config.cookies_options import get_cookie_options
from app.core.settings import SettingsService


class CookieService:
    """
    Manages authentication cookies.

    Responsible only for writing and removing authentication
    cookies from HTTP responses.

    Cookie security configuration is delegated to
    `get_cookie_options()`.
    """

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(
        self,
        settings: SettingsService,
    ) -> None:
        """
        Initializes the cookie service.

        Settings are injected by the application container.
        """

        self.settings = settings

    # ============================================================
    # SET AUTH COOKIES
    # ============================================================

    def set_auth_cookies(
        self,
        response: Response,
        access_token: str,
        refresh_token: str,
    ) -> None:
        """
        Stores the access and refresh tokens in HTTP-only cookies.

        Access token:
            Short-lived cookie used for authenticated API requests.

        Refresh token:
            Long-lived cookie used to obtain a new access token.

        Tokens are never exposed to JavaScript because the cookies
        are configured with HttpOnly.
        """

        access_options = get_cookie_options(
            minutes=self.settings.jwt_access_cookie_expire_in,
            settings=self.settings,
        )

        refresh_options = get_cookie_options(
            minutes=self.settings.jwt_refresh_cookie_expire_in,
            settings=self.settings,
        )

        response.set_cookie(
            key="access_token",
            value=access_token,
            **access_options,
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            **refresh_options,
        )

    # ============================================================
    # CLEAR AUTH COOKIES
    # ============================================================

    def clear_auth_cookies(
        self,
        response: Response,
    ) -> None:
        """
        Removes all authentication cookies.

        Used during logout or when the authentication state
        must be terminated.
        """

        response.delete_cookie(
            key="access_token",
            path="/",
        )

        response.delete_cookie(
            key="refresh_token",
            path="/",
        )

