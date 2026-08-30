# app/db/transactions/dependencies.py

from typing import Annotated
from app.core.container import Container
from fastapi import Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.transactions.sqlalchemy_unit_of_work import (
    SQLAlchemyUnitOfWork,
)
from app.db.transactions.unit_of_work import UnitOfWork



# ============================================================
# CONTAINER DEPENDENCY
# ============================================================

def get_container(
    request: Request,
) -> Container:
    """
    Retrieves the application dependency container.

    The container owns application-wide dependencies such as:

    - application settings
    - database session management
    - shared security services
    - external clients
    """

    return request.app.state.container


# ============================================================
# DATABASE SESSION DEPENDENCY
# ============================================================

async def get_db_session(
    container: Annotated[
        Container,
        Depends(get_container),
    ],
):
    """
    Provides an asynchronous database session.

    All repositories participating in the same authentication
    operation receive the same AsyncSession.
    """

    async for session in container.db_session.get_session():
        yield session


# ============================================================
# UNIT OF WORK DEPENDENCY
# ============================================================

def get_unit_of_work(
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
) -> UnitOfWork:
    """
    Provides the application's UnitOfWork abstraction.

    The UnitOfWork is created from the current database session.

    The same AsyncSession is therefore used by the UnitOfWork
    and by the repositories participating in the transaction.

    The dependency returns the abstraction rather than the concrete
    SQLAlchemy implementation so that application services remain
    independent from SQLAlchemy.
    """

    return SQLAlchemyUnitOfWork(
        session=session,
    )