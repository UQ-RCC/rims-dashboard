import typing
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative, declarative_base, declared_attr
#from sqlalchemy.orm import sessionmaker
from fastapi_utils.session import FastAPISessionMaker
import rimsdash.config as config

from functools import lru_cache

SQLALCHEMY_DATABASE_URL = (f"{config.get('database', 'type', required=True)}://"
                            f"{config.get('database', 'db_username', required=True)}:"
                            f"{config.get('database', 'db_password', required=True)}@"
                            f"{config.get('database', 'host', required=True)}:"
                            f"{config.get('database', 'port', required=True)}/"
                            f"{config.get('database', 'db_name', required=True)}")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={},
)

# stock alternative:
#Base = declarative_base()

@lru_cache()
def _get_fastapi_sessionmaker() -> FastAPISessionMaker:
    """ This function could be replaced with a global variable if preferred """
    return FastAPISessionMaker(SQLALCHEMY_DATABASE_URL)


sessionmaker = _get_fastapi_sessionmaker()

def get_session():
    with sessionmaker.context_session() as db:
        return db

