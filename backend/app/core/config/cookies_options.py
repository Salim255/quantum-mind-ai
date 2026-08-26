from typing import Any

from app.core.settings import SettingsService


def get_cookie_options(
    minutes: int,
    settings: SettingsService,
) -> dict[str, Any]:
    """
    Creates secure HTTP cookie options.

    The application settings determine whether the application is
    running in production.

    Args:
        minutes:
            Cookie lifetime expressed in minutes.

        settings:
            Application settings used to determine the cookie
            security configuration.

    Returns:
        A dictionary compatible with FastAPI/Starlette
        `Response.set_cookie()`.

    Important:
        FastAPI expects `max_age` in seconds.
    """

    return {
        "httponly": True,

        # Secure cookies require HTTPS.
        # Enabled only in production.
        "secure": settings.is_production,

        # Production uses Lax for normal browser navigation.
        # Development uses Strict for stronger local protection.
        "samesite": (
            "lax"
            if settings.is_production
            else "strict"
        ),

        # FastAPI expects seconds.
        "max_age": minutes * 60,

        # Cookie available to the entire application.
        "path": "/",
    }