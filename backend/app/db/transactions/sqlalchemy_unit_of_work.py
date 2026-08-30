# app/db/transactions/sqlalchemy_unit_of_work.py

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.transactions.unit_of_work import UnitOfWork


class SQLAlchemyUnitOfWork(UnitOfWork):
    """
    SQLAlchemy implementation of the Unit of Work pattern.

    This class manages the lifecycle of a single SQLAlchemy
    database session and its transaction.

    The Unit of Work provides a transaction boundary around
    multiple repository operations.

    Example:

        async with SQLAlchemyUnitOfWork(session) as uow:

            await repository.operation_1()

            await repository.operation_2()

            await repository.operation_3()

    If every operation succeeds:

        COMMIT

    If any operation raises an exception:

        ROLLBACK

    The repositories do not decide when to commit or rollback.
    The Unit of Work owns that responsibility.
    """

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        """
        Initializes the Unit of Work with an existing SQLAlchemy
        database session.

        The session is provided from the application's database
        session infrastructure.

        The Unit of Work does not create the session itself.
        It only controls the transaction lifecycle of that session.
        """

        self.session = session

    # ============================================================
    # ENTER TRANSACTION
    # ============================================================

    async def __aenter__(self):
        """
        Enters the Unit of Work transaction context.

        This method is executed when Python enters:

            async with unit_of_work:

        We begin a SQLAlchemy transaction here.

        Returning self allows the caller to access the Unit of Work
        instance inside the context:

            async with unit_of_work as uow:
                ...
        """

        await self.session.begin()

        return self

    # ============================================================
    # EXIT TRANSACTION
    # ============================================================

    async def __aexit__(
        self,
        exception_type,
        exception_value,
        traceback,
    ):
        """
        Exits the Unit of Work transaction context.

        Python automatically provides information about whether
        an exception occurred inside the transaction.

        No exception:

            exception_type is None

        Exception:

            exception_type is not None

        Successful execution results in COMMIT.

        Failed execution results in ROLLBACK.

        The session is closed after the transaction finishes.
        """

        try:

            # ----------------------------------------------------
            # ROLLBACK ON FAILURE
            # ----------------------------------------------------

            if exception_type is not None:

                await self.session.rollback()

                # Returning False tells Python that the original
                # exception must continue propagating to the caller.
                return False

            # ----------------------------------------------------
            # COMMIT ON SUCCESS
            # ----------------------------------------------------

            await self.session.commit()

            return False

        finally:

            # ----------------------------------------------------
            # CLOSE SESSION
            # ----------------------------------------------------

            await self.session.close()