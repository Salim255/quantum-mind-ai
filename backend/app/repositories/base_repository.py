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
        entity: T
    ) -> T:
        """
        Add a new entity and persist it.
        """

        self.session.add(entity)

        await self.session.commit()

        await self.session.refresh(entity)

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