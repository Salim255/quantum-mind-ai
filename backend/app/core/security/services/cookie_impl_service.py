from fastapi import Response, Request

from app.core.config.cookies_options import get_cookie_options
from app.core.settings import SettingsService
from app.common.constants import ( ACCESS_TOKEN_COOKIE, REFRESH_TOKEN_COOKIE )
from app.core.security.services.cookie_service import CookieService

class CookieImplService(CookieService):
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
        self.ACCESS_TOKEN_COOKIE =   ACCESS_TOKEN_COOKIE

        self.REFRESH_TOKEN_COOKIE = REFRESH_TOKEN_COOKIE

        self.settings = settings


   # ============================================================
    # GET ACCESS TOKEN
    # ============================================================

    def get_access_token(
        self,
        request: Request,
    ) -> str | None:
        """
        Retrieves the access token from the incoming request.

        The access token is stored in an HttpOnly cookie.

        Args:
            request:
                Incoming HTTP request containing the authentication
                cookies.

        Returns:
            The access token when the cookie exists.
            None when the access-token cookie is not present.
        """

        return request.cookies.get(
            self.ACCESS_TOKEN_COOKIE,
        )
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
            minutes=self.settings.JWT_ACCESS_COOKIE_EXPIRE_IN,
            settings=self.settings,
        )

        refresh_options = get_cookie_options(
            minutes=self.settings.JWT_REFRESH_COOKIE_EXPIRE_IN,
            settings=self.settings,
        )

        response.set_cookie(
            key=self.ACCESS_TOKEN_COOKIE,
            value=access_token,
            **access_options,
        )

        response.set_cookie(
            key=self.REFRESH_TOKEN_COOKIE,
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
            key=self.ACCESS_TOKEN_COOKIE,
            path="/",
        )

        response.delete_cookie(
            key=self.REFRESH_TOKEN_COOKIE,
            path="/",
        )

