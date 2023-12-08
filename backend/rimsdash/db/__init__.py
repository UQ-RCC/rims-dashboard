# from .database import SessionLocal, engine
from typing import Generator, Optional

from .base import Base
from .session import engine
from .session import _get_fastapi_sessionmaker, get_session, sessionmaker
#from .init_db import initialise_db
from typing import Iterator
from sqlalchemy.orm import Session


def exists() -> bool:
    """
    simple check for user table to determine if DB has been created
    """
    with engine.connect() as connection:
        return engine.dialect.has_table(connection, 'rduser')

def init_db():
    print("Initialising DB")    
    Base.metadata.create_all(bind=engine)

def get_db() -> Iterator[Session]:
    """ FastAPI dependency that provides a sqlalchemy session """
    yield from _get_fastapi_sessionmaker().get_db()

    # get_db() -> generator
    # get session via next(rdb.get_db())

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