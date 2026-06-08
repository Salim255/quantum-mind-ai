from typing import Generic, TypeVar, Type, Optional, List
from sqlmodel import Session, select

# Generic type for any model (Topic, User, etc.)
T = TypeVar("T")


class BaseRepository(Generic[T]):
    """
    Base repository that handles common database operations.

    This avoids repeating CRUD logic in every repository.
    """

    def __init__(self, session: Session, model: Type[T]):
        # DB session (connection to database)
        self.session = session

        # The model this repository works with (e.g. Topic)
        self.model = model

    # -----------------------------
    # GET BY ID
    # -----------------------------
    def get_by_id(self, id) -> Optional[T]:
        """
        Fetch a single record by primary key.
        """
        statement = select(self.model).where(self.model.id == id)
        return self.session.exec(statement).first()

    # -----------------------------
    # GET ALL
    # -----------------------------
    def get_all(self) -> List[T]:
        """
        Fetch all records from table.
        """
        statement = select(self.model)
        return self.session.exec(statement).all()

    # -----------------------------
    # ADD / CREATE
    # -----------------------------
    def add(self, entity: T) -> T:
        """
        Insert new record into database.
        """
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    # -----------------------------
    # DELETE
    # -----------------------------
    def delete(self, entity: T) -> None:
        """
        Remove record from database.
        """
        self.session.delete(entity)
        self.session.commit()