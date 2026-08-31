from collections.abc import Awaitable, Callable

from fastapi import Request, Response

from app.core.exceptions.custom_exceptions import UnauthorizedException
from app.v1.modules.auth.services.cookie_service import CookieService
from app.v1.modules.auth.services.jwt_manager_service import JWTManagerService


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
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """
        Processes an incoming HTTP request.

        `call_next` represents the next step in the FastAPI
        request pipeline.

        Calling:

            await call_next(request)

        allows the request to continue toward the endpoint.

        Not calling it means the request is stopped here.
        """

        # ----------------------------------------------------
        # PUBLIC ROUTE CHECK
        # ----------------------------------------------------

        # Public endpoints do not require authentication.
        #
        # We therefore immediately allow the request to continue.
        if self._is_public_route(request):
            return await call_next(request)

        # ----------------------------------------------------
        # ACCESS TOKEN EXTRACTION
        # ----------------------------------------------------

        # Authentication credentials are stored in the
        # HttpOnly access-token cookie.
        access_token = self.cookie_service.get_access_token(
            request=request,
        )

        # ----------------------------------------------------
        # TOKEN EXISTENCE CHECK
        # ----------------------------------------------------

        # A protected endpoint cannot be accessed without
        # an access token.
        if access_token is None:
            raise UnauthorizedException(
                message="Authentication required.",
            )

        # ----------------------------------------------------
        # TOKEN VERIFICATION
        # ----------------------------------------------------

        # JWTManagerService owns the JWT verification logic.
        #
        # It verifies things such as:
        #
        # - JWT signature
        # - expiration
        # - token structure
        # - required claims
        #
        # If verification fails, the request is rejected.
        self.jwt_manager_service.verify_access_token(
            access_token,
        )

        # ----------------------------------------------------
        # AUTHENTICATION SUCCESSFUL
        # ----------------------------------------------------

        # The token is valid.
        #
        # The request is therefore allowed to continue through
        # the remaining FastAPI request pipeline.
        return await call_next(request)

    def _is_public_route(
        self,
        request: Request,
    ) -> bool:
        """
        Determines whether the current endpoint is public.

        This method will later use the application's public-route
        metadata/decorator instead of maintaining a hard-coded
        list of URLs.
        """

        return False