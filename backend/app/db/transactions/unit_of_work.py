from abc import ABC, abstractmethod


class UnitOfWork(ABC):
    """
    Defines the Unit of Work contract.

    A Unit of Work represents a single database transaction boundary.

    Its responsibility is to guarantee that a group of database
    operations is treated as one atomic operation:

        BEGIN TRANSACTION
            operation 1
            operation 2
            operation 3
        COMMIT

    If an unexpected error occurs:

        BEGIN TRANSACTION
            operation 1
            operation 2
            operation 3
        ROLLBACK

    This abstraction intentionally does not know anything about
    SQLAlchemy, repositories, or specific database implementations.

    The concrete implementation will be responsible for managing
    the actual database session and transaction.
    """

    # ============================================================
    # ENTER TRANSACTION
    # ============================================================

    @abstractmethod
    async def __aenter__(self):
        """
        Starts the Unit of Work context.

        This method is called when entering:

            async with unit_of_work:

        The concrete implementation can use this point to:

        - create or acquire a database session
        - begin a transaction
        - prepare the transaction context

        The Unit of Work instance itself is returned so that the
        caller can access it inside the context if necessary.

        Example:

            async with unit_of_work as uow:
                ...

        """

        raise NotImplementedError

    # ============================================================
    # EXIT TRANSACTION
    # ============================================================

    @abstractmethod
    async def __aexit__(
        self,
        exception_type,
        exception_value,
        traceback,
    ):
        """
        Finishes the Unit of Work context.

        This method is called automatically when leaving:

            async with unit_of_work:
                ...

        Python passes information about any exception raised inside
        the context.

        If no exception occurred:

            exception_type = None
            exception_value = None
            traceback = None

        The implementation should then COMMIT the transaction.

        If an exception occurred:

            exception_type is not None

        The implementation should then ROLLBACK the transaction.

        This gives us the atomic behavior we want:

            success
                -> COMMIT

            failure
                -> ROLLBACK

        The Unit of Work therefore becomes the boundary that decides
        whether all database changes are persisted or none of them
        are persisted.
        """

        raise NotImplementedError