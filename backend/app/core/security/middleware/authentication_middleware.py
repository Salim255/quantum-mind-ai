from collections.abc import Awaitable, Callable

from fastapi import Request, Response

from app.core.exceptions.custom_exceptions import (
    ProcessingException,
    UnauthorizedException,
)

from app.v1.modules.auth.services.cookie_service import (
    CookieService,
)

from app.v1.modules.auth.services.jwt_manager_service import (
    JWTManagerService,
)


class AuthenticationMiddleware:
    """
    Global authentication middleware.

    This middleware acts as the application's first authentication
    gate.

    Every incoming HTTP request passes through this middleware
    before reaching the requested endpoint.

    The middleware is responsible for:

    1. Determining whether the endpoint is public.
    2. Extracting the access token from the authentication cookie.
    3. Verifying the access token.
    4. Rejecting unauthenticated requests.
    5. Allowing authenticated requests to continue.

    The middleware does NOT:

    - create users
    - perform login
    - issue tokens
    - manage passwords
    - perform authorization
    - contain JWT cryptographic logic

    Those responsibilities remain inside their respective services.
    """

    def __init__(
        self,
        cookie_service: CookieService,
        jwt_manager_service: JWTManagerService,
    ) -> None:
        """
        Initializes the authentication middleware.

        CookieService
            Responsible for authentication cookie management.

        JWTManagerService
            Responsible for validating and decoding JWT tokens.
        """

        self.cookie_service = cookie_service
        self.jwt_manager_service = jwt_manager_service

    async def __call__(
        self,
        request: Request,
        call_next: Callable[
            [Request],
            Awaitable[Response],
        ],
    ) -> Response:
        """
        Processes an incoming HTTP request.

        The middleware first determines whether the requested
        endpoint is public.

        Protected endpoints must provide a valid access token
        through the authentication cookie.

        Only successfully authenticated requests are passed
        to the next stage of the request pipeline.
        """

        # ====================================================
        # PUBLIC ROUTE
        # ====================================================

        try:
            # Public endpoints do not require authentication.

            if self._is_public_route(request):
                return await call_next(request)

        except Exception as exc:
            raise ProcessingException(
                message="Unable to determine route authentication status.",
            ) from exc

        # ====================================================
        # AUTHENTICATION
        # ====================================================

        try:
            # ------------------------------------------------
            # ACCESS TOKEN EXTRACTION
            # ------------------------------------------------

            # Authentication credentials are stored inside
            # the HttpOnly access-token cookie.
            access_token = self.cookie_service.get_access_token(
                request=request,
            )

            # ------------------------------------------------
            # TOKEN EXISTENCE CHECK
            # ------------------------------------------------

            # A protected endpoint cannot be accessed without
            # an access token.
            if access_token is None:
                raise UnauthorizedException(
                    message="Authentication required.",
                )

            # ------------------------------------------------
            # TOKEN VERIFICATION
            # ------------------------------------------------

            # JWTManagerService owns the JWT verification logic.
            #
            # It verifies:
            #
            # - JWT signature
            # - token expiration
            # - token structure
            # - required claims
            #
            # If the token is invalid, the JWT manager raises
            # the appropriate authentication exception.
            self.jwt_manager_service.verify_access_token(
                access_token,
            )

        except UnauthorizedException:
            # Authentication failures are expected application
            # errors.
            #
            # Re-raise them unchanged so the application's
            # exception handler can convert them into the
            # appropriate HTTP response.
            raise

        except Exception as exc:
            # Any unexpected error occurring during authentication
            # is converted into the application's standard
            # processing exception.
            raise ProcessingException(
                message="Unable to process authentication request.",
            ) from exc

        # ====================================================
        # CONTINUE REQUEST PIPELINE
        # ====================================================

        # Authentication succeeded.
        #
        # IMPORTANT:
        # `call_next()` is intentionally outside the authentication
        # try/except block.
        #
        # Therefore, if the controller or another downstream
        # service raises an exception, that exception is handled
        # by the application's normal exception handling system
        # instead of being incorrectly treated as an authentication
        # error.
        return await call_next(request)

    def _is_public_route(
        self,
        request: Request,
    ) -> bool:
        """
        Determines whether the current endpoint is public.

        This method will later use endpoint metadata created by
        the application's public-route mechanism.

        It should NOT contain a hard-coded list of URLs.
        """

        return False