from abc import ABC, abstractmethod

from fastapi import Response, Request


class CookieService(ABC):
    """
    Defines the contract for authentication cookie management.

    The service is responsible for setting and clearing authentication
    cookies without exposing the underlying HTTP implementation to
    the authentication business logic.
    """


    # ============================================================
    # GET ACCESS TOKEN
    # ============================================================

    @abstractmethod
    def get_access_token(
        self,
        request: Request,
    ) -> str | None:
        """
        Retrieves the access token from the incoming HTTP request.

        The access token is stored inside the authentication cookie.

        Args:
            request:
                Incoming HTTP request containing the cookies.

        Returns:
            The access token when the authentication cookie exists.
            None when the cookie is not present.
        """

        raise NotImplementedError
    

    # ============================================================
    # SET AUTHENTICATION COOKIES
    # ============================================================

    @abstractmethod
    def set_auth_cookies(
        self,
        response: Response,
        access_token: str,
        refresh_token: str,
    ) -> None:
        """
        Sets the authentication cookies.

        Args:
            response:
                HTTP response receiving the cookies.

            access_token:
                Short-lived access token.

            refresh_token:
                Long-lived refresh token.
        """

        raise NotImplementedError

    # ============================================================
    # CLEAR AUTHENTICATION COOKIES
    # ============================================================

    @abstractmethod
    def clear_auth_cookies(
        self,
        response: Response,
    ) -> None:
        """
        Clears all authentication cookies.

        Typically called during logout or when the authentication
        session must be terminated.
        """

        raise NotImplementedError