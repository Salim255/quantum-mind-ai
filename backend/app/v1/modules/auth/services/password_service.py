from abc import ABC, abstractmethod


class PasswordService(ABC):
    """
    Defines the contract for password hashing and verification.

    Authentication services depend on this abstraction rather than
    directly depending on the password-hashing library.

    Responsibilities:

    - Hash plaintext passwords before persistence.
    - Verify plaintext passwords against stored password hashes.

    Plaintext passwords must never be stored, logged, or returned
    from the application.
    """

    # ============================================================
    # HASH
    # ============================================================

    @abstractmethod
    def hash_password(
        self,
        password: str,
    ) -> str:
        """
        Creates a secure password hash.

        The returned value is safe to persist in the database.

        Args:
            password:
                Plaintext password supplied by the user.

        Returns:
            Secure password hash.
        """

        raise NotImplementedError

    # ============================================================
    # VERIFY
    # ============================================================

    @abstractmethod
    def verify_password(
        self,
        password: str,
        password_hash: str,
    ) -> bool:
        """
        Verifies a plaintext password against a stored hash.

        Args:
            password:
                Plaintext password supplied during authentication.

            password_hash:
                Previously stored password hash.

        Returns:
            True when the password matches.
            False otherwise.
        """

        raise NotImplementedError