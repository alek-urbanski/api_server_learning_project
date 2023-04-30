from typing import AsyncIterator, Callable
import sqlalchemy
from sqlalchemy import orm
from app.db import base_db_model

Session = orm.Session  # type alias, to detach apis from sqlalchemy

engine: sqlalchemy.Engine
LocalSession: Callable[[], orm.Session] = orm.sessionmaker()  # session factory


async def init(database_filename: str) -> None:
    """Creates a global database engine and binds it to the global sessionmaker object."""
    global engine
    engine = sqlalchemy.create_engine(database_filename)
    base_db_model.Base.metadata.bind = engine  # type: ignore
    base_db_model.Base.metadata.create_all(bind=engine)
    LocalSession.configure(bind=engine)


async def get_db() -> AsyncIterator[Session]:
    """Yields the new session and closes it at the end.
    This way I don't need to close sessions anywhere else in the code."""
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
