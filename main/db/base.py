from typing import Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from main.core.config import get_app_settings

settings = get_app_settings()

engine = create_engine(url=settings.database_url, echo=True, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: Any = declarative_base()


def get_db() -> Generator:
    """
    Generator dependency yield database connection.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()