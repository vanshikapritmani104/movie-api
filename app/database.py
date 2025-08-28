from typing import Iterator
from sqlmodel import SQLModel, create_engine, Session
from .config import settings

# For SQLite, check_same_thread must be False
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, echo=False, connect_args=connect_args)

def get_session() -> Iterator[Session]:
    """Dependency that provides a database session."""
    with Session(engine) as session:
        yield session

def init_db() -> None:
    """Initialize the database and create all tables."""
    SQLModel.metadata.create_all(engine)