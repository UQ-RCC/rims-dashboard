# from .database import SessionLocal, engine
from .database import engine, Base
from .database import _get_fastapi_sessionmaker
from typing import Iterator
from sqlalchemy.orm import Session

from rimsdash.models import User, Project, System

Base.metadata.create_all(bind=engine)

def get_db() -> Iterator[Session]:
    """ FastAPI dependency that provides a sqlalchemy session """
    yield from _get_fastapi_sessionmaker().get_db()