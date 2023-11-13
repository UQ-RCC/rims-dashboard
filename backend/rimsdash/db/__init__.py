# from .database import SessionLocal, engine
from typing import Generator, Optional

from .base import Base
from .session import engine
from .session import _get_fastapi_sessionmaker
#from .init_db import initialise_db
from typing import Iterator
from sqlalchemy.orm import Session


def init_db():
    Base.metadata.create_all(bind=engine)

def get_db() -> Iterator[Session]:
    """ FastAPI dependency that provides a sqlalchemy session """
    yield from _get_fastapi_sessionmaker().get_db()

def drop_db(force = False):
    """
    drop the db
    """
    if force:
        print("DROPPING DATABASE")
        Base.metadata.drop_all(bind=engine)
    
    #NB: because our data is just a local cache/derivation from the external DB, don't really need to worry about migrations
    #   to modify a table, just drop and recreate it

"""
#ALT:
def get_db() -> Generator:
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()
"""    

print("starting DB")
init_db()