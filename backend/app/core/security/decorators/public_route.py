from functools import wraps


def public_route(func):
    """
    Marks an endpoint as publicly accessible.

    This decorator does not perform authentication and does not
    modify the endpoint's business behavior.

    Its only responsibility is to attach metadata to the endpoint
    indicating that authentication is not required.

    The global AuthenticationMiddleware is responsible for reading
    this metadata and deciding whether the request must pass
    authentication.

    Therefore:

        @public_route
        async def register(...):
            ...

    means:

        Request
            │
            ▼
        AuthenticationMiddleware
            │
            ├── Public endpoint
            │       │
            │       ▼
            │    Allow request
            │
            └── Protected endpoint
                    │
                    ▼
                Verify access token
                    │
                    ├── Invalid → Reject request
                    │
                    └── Valid → Allow request

    The decorator itself does NOT:

    - read authentication cookies
    - decode JWT tokens
    - validate JWT signatures
    - authenticate users
    - perform authorization
    - raise authentication exceptions
    - communicate with the database

    Authentication responsibilities remain inside the
    AuthenticationMiddleware and its security services.

    Args:
        func:
            The FastAPI endpoint function being marked as public.

    Returns:
        The original endpoint function with public-route metadata
        attached.

    The `@wraps` decorator preserves the original endpoint's
    metadata, including its name, documentation, and annotations,
    which is important for FastAPI's route inspection and
    OpenAPI generation.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Preserves the original endpoint behavior.

        The wrapper does not introduce any authentication logic.
        It simply forwards the call to the original endpoint.
        """

        return func(*args, **kwargs)

    # ------------------------------------------------------------
    # PUBLIC ROUTE METADATA
    # ------------------------------------------------------------

    # This flag is consumed by the authentication mechanism to
    # identify endpoints that do not require authentication.
    #
    # Keeping the value as metadata makes the decorator itself
    # independent from the authentication implementation.
    wrapper.__public_route__ = True

    return wrapper