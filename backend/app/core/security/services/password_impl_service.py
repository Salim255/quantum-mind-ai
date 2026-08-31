from pwdlib import PasswordHash

from app.core.security.services.password_service import PasswordService


class PasswordImplService(PasswordService):
    """
    Password hashing implementation using pwdlib.

    pwdlib provides a modern password-hashing abstraction and uses
    Argon2 as the recommended password hashing algorithm.

    This class keeps all password-library-specific logic isolated
    from the authentication service.
    """

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(self) -> None:
        """
        Initializes the password hashing service.

        PasswordHash.recommended() configures the recommended
        password hashing algorithm and parameters.
        """

        self._password_hash = PasswordHash.recommended()

    # ============================================================
    # HASH
    # ============================================================

    def hash_password(
        self,
        password: str,
    ) -> str:
        """
        Hashes a plaintext password.

        A unique salt is automatically generated as part of the
        password hashing process.

        The plaintext password is never persisted.
        """

        return self._password_hash.hash(password)

    # ============================================================
    # VERIFY
    # ============================================================

    def verify_password(
        self,
        password: str,
        password_hash: str,
    ) -> bool:
        """
        Verifies a plaintext password against its stored hash.

        Returns False when the password does not match.
        """

        return self._password_hash.verify(
            password,
            password_hash,
        )