from typing import Generic, TypeVar, Type, Optional, List
from uuid import UUID
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession


T = TypeVar("T")


class BaseRepository(Generic[T]):
    """
    Async base repository that provides common CRUD operations.

    All repositories inherit from this class to avoid
    duplicating database access logic.
    """

    def __init__(
        self,
        session: AsyncSession,
        model: Type[T],
    ):
        self.session = session
        self.model = model


    # --------------------------------------------------
    # GET BY USER ID
    # --------------------------------------------------
    async def get_by_user_id(
        self,
        user_id: UUID
    ) -> Optional[T]:
        """
        Fetch one entity by user id.
        """

        statement = select(self.model).where(
            self.model.user_id == user_id
        )

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    # --------------------------------------------------
    # GET BY ID
    # --------------------------------------------------

    async def get_by_id(
        self,
        id: UUID
    ) -> Optional[T]:
        """
        Fetch one entity by primary key.
        """

        statement = select(self.model).where(
            self.model.id == id
        )

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()


    # --------------------------------------------------
    # GET ALL
    # --------------------------------------------------

    async def get_all(self) -> List[T]:
        """
        Fetch all entities.
        """

        statement = select(self.model)

        result = await self.session.execute(statement)

        return list(result.scalars().all())


    # --------------------------------------------------
    # ADD / CREATE
    # --------------------------------------------------

    async def add(
        self,
        entity: T,
    ) -> T:
        """
        Adds an entity to the current database transaction.

        This method does not commit the transaction.

        The repository is responsible only for adding the entity
        to the current SQLAlchemy session and synchronizing it with
        the database.

        Transaction ownership belongs to the application layer,
        typically through UnitOfWork.

        The operation works as follows:

        1. session.add(entity)
        Registers the entity with the current SQLAlchemy session.

        2. session.flush()
        Sends the INSERT statement to the database without committing
        the transaction.

        This allows the database to generate values such as:

            - primary keys
            - server-generated fields

        while keeping the transaction open.

        3. session.refresh(entity)
        Reloads the entity from the database so the returned object
        contains the latest persisted values.

        4. return entity
        Returns the entity to the calling service.

        The transaction remains open after this method returns.

        The UnitOfWork is responsible for ultimately deciding whether
        the transaction should be committed or rolled back.
        """

        # ------------------------------------------------------------
        # ADD ENTITY TO SESSION
        # ------------------------------------------------------------

        # Register the entity with the current SQLAlchemy session.
        #
        # At this point, no SQL INSERT is necessarily sent to the
        # database yet.
        self.session.add(entity)

        # ------------------------------------------------------------
        # FLUSH CHANGES
        # ------------------------------------------------------------

        # Send the pending INSERT to the database without committing
        # the current transaction.
        #
        # This is important because database-generated values, such
        # as the entity's primary key, may now become available.
        await self.session.flush()

        # ------------------------------------------------------------
        # REFRESH ENTITY
        # ------------------------------------------------------------

        # Reload the entity from the database so the Python object
        # contains the latest database state and any generated values.
        await self.session.refresh(entity)

        # ------------------------------------------------------------
        # RETURN ENTITY
        # ------------------------------------------------------------

        # Return the entity while leaving transaction ownership to
        # the caller / UnitOfWork.
        return entity


    # --------------------------------------------------
    # UPDATE
    # --------------------------------------------------

    async def update(
        self,
        entity: T,
    ) -> T:
        """
        Persist changes made to an existing entity.
        """

        self.session.add(entity)

        await self.session.commit()

        await self.session.refresh(entity)

        return entity

    # --------------------------------------------------
    # DELETE
    # --------------------------------------------------

    async def delete(
        self,
        entity: T
    ) -> None:
        """
        Delete an entity.
        """

        self.session.delete(entity)

        await self.session.commit()