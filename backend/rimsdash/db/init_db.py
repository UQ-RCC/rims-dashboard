import logging
from sqlalchemy.orm import Session

from .base import Base
from .session import engine

logger = logging.getLogger(__name__)

def initialise_db(db: Session) -> None:
    Base.metadata.create_all(bind=engine)