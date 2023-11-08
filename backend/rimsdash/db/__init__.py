# from .database import SessionLocal, engine
from typing import Generator, Optional

from .base import Base
from .session import engine
from .session import _get_fastapi_sessionmaker
#from .init_db import initialise_db
from typing import Iterator
from sqlalchemy.orm import Session

print("creating")
Base.metadata.create_all(bind=engine)

def get_db() -> Iterator[Session]:
    """ FastAPI dependency that provides a sqlalchemy session """
    yield from _get_fastapi_sessionmaker().get_db()

"""
#ALT:
def get_db() -> Generator:
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()
"""    