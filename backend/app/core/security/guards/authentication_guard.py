from fastapi import Request

from app.core.exceptions.custom_exceptions import (
    ProcessingException,
    UnauthorizedException,
)

from app.core.security.services.cookie_service import (
    CookieService,
)

from app.core.security.services.jwt_manager_service import (
    JWTManagerService,
)


class AuthenticationGuard:
    """
    Authentication guard responsible for protecting HTTP requests.

    Unlike ASGI middleware, this guard executes inside FastAPI's
    dependency lifecycle.

    This is important because FastAPI has already resolved the
    request route when the dependency executes. The guard can
    therefore be attached explicitly to protected endpoints or
    routers without having to resolve route metadata at the
    middleware level.

    Request flow:

        Client
          │
          ▼
        FastAPI
          │
          ▼
        AuthenticationGuard
          │
          ├── No access token ─────► UnauthorizedException
          │
          ├── Invalid token ───────► UnauthorizedException
          │
          ├── Authentication error ► ProcessingException
          │
          └── Valid token
                    │
                    ▼
               Controller


    Responsibilities
    ----------------

    The guard is responsible for:

    - retrieving the access token from the request
    - verifying the access token
    - stopping unauthenticated requests
    - allowing authenticated requests to continue


    The guard does NOT:

    - register users
    - authenticate login credentials
    - create users
    - create sessions
    - issue tokens
    - refresh tokens
    - manage passwords
    - perform authorization
    - implement JWT cryptography
    - access the dependency container


    Those responsibilities belong to the appropriate services.

    Dependency architecture:

        Application Container
                 │
                 ├── CookieService
                 │
                 └── JWTManagerService
                         │
                         ▼
                AuthenticationGuard
                         │
                         ▼
                  FastAPI Dependency
                         │
                         ▼
                     Controller
    """

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(
        self,
        cookie_service: CookieService,
        jwt_manager_service: JWTManagerService,
    ) -> None:
        """
        Initializes the authentication guard.

        Dependencies are injected during application assembly.

        The guard intentionally does not receive the application
        container. This keeps the guard independent from the
        dependency-injection implementation.

        Args:
            cookie_service:
                Responsible for retrieving the authentication
                token from the incoming request.

            jwt_manager_service:
                Responsible for validating the JWT access token.
        """

        self.cookie_service = cookie_service
        self.jwt_manager_service = jwt_manager_service

    # ============================================================
    # AUTHENTICATE REQUEST
    # ============================================================

    async def __call__(
        self,
        request: Request,
    ) -> None:
        """
        Authenticates the current HTTP request.

        This method is intended to be used as a FastAPI dependency
        for protected endpoints.

        Authentication flow:

            Request
                │
                ▼
            CookieService
                │
                ├── No token ──────► UnauthorizedException
                │
                ▼
            JWTManagerService
                │
                ├── Invalid ───────► UnauthorizedException
                │
                └── Valid
                     │
                     ▼
                  Controller


        Returns:
            None when authentication succeeds.

        Raises:
            UnauthorizedException:
                When the request does not contain a valid
                authentication token.

            ProcessingException:
                When an unexpected infrastructure error occurs
                while processing authentication.
        """

        try:

            # ====================================================
            # GET ACCESS TOKEN
            # ====================================================

            # The authentication token is stored in the
            # HttpOnly authentication cookie.
            #
            # CookieService owns all cookie-related details.
            #
            # The guard therefore does not need to know:
            #
            # - the cookie name
            # - cookie attributes
            # - SameSite configuration
            # - Secure configuration
            # - HttpOnly configuration
            #
            # It only asks the service for the access token.
            access_token = self.cookie_service.get_access_token(
                request=request,
            )

            # ====================================================
            # ACCESS TOKEN REQUIRED
            # ====================================================

            # A protected endpoint requires authentication.
            #
            # No token means the request cannot be authenticated.
            #
            # UnauthorizedException is intentionally allowed to
            # propagate to FastAPI's global exception handler.
            if access_token is None:
                raise UnauthorizedException(
                    message="Authentication required.",
                )

            # ====================================================
            # VERIFY ACCESS TOKEN
            # ====================================================

            # Retrieving the token is NOT authentication.
            #
            # The token must be cryptographically and semantically
            # validated before the request can be considered
            # authenticated.
            #
            # JWTManagerService owns all JWT implementation details.
            #
            # It is responsible for validating things such as:
            #
            # - JWT structure
            # - signature
            # - expiration
            # - algorithm
            # - required claims
            #
            # If the token is invalid or expired, the JWT manager
            # should raise UnauthorizedException.
            self.jwt_manager_service.verify_access_token(
                access_token,
            )

        except UnauthorizedException:
            # ====================================================
            # EXPECTED AUTHENTICATION FAILURE
            # ====================================================

            # This is an expected application-level exception.
            #
            # DO NOT convert it into ProcessingException.
            #
            # Let the global application exception handler process
            # it and return the appropriate HTTP 401 response.
            raise

        except Exception as exc:
            # ====================================================
            # UNEXPECTED AUTHENTICATION FAILURE
            # ====================================================

            # Something unexpected happened inside the
            # authentication infrastructure.
            #
            # Do not expose the internal exception to the client.
            #
            # Convert it into the application's generic processing
            # exception while preserving the original exception
            # through exception chaining for internal debugging
            # and logging.
            raise ProcessingException(
                message="Unable to process authentication request.",
            ) from exc

        # ========================================================
        # AUTHENTICATION SUCCESSFUL
        # ========================================================

        # No value needs to be returned.
        #
        # The absence of an exception means authentication
        # succeeded, so FastAPI continues with the remaining
        # dependencies and eventually executes the controller.
        return