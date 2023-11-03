import enum, datetime
from sqlalchemy.orm import aliased, Session
from . import models, schemas
import logging
logger = logging.getLogger('rimsdash')


#utils

def row2dict(row, keep_id = True):
    d = {}
    for column in row.__table__.columns:
        if column.name == 'id' and not keep_id:
            continue
        else:
            row_val = getattr(row, column.name)
            if isinstance(row_val, enum.Enum):
                row_val = row_val.value
            d[column.name] = row_val
    return d

#systems

def clear_systems(db: Session):
    db.query(models.System).delete()

def get_all_systems(db: Session):
    return db.query(models.System).all()

def get_system(db: Session, id: int):
    return db.query(models.System).\
            filter(models.System.id == id).first()

def update_system(db: Session, system: schemas.System):
    """
    Update an existing system, or create it if missing
    """
    #look for the system in the DB
    _system = get_system(db, system.id)

    #if it exists, update it
    if _system:
        _system.id = system.id
        _system.name = system.name
        _system.type = system.type
        db.commit()
        db.refresh(_system)
    #otherwise create it
    else:
        _system = models.System(**system.dict())
        db.add(_system)
        #db.commit()
        db.flush()
        db.refresh(_system)
    return _system


def get_user(db: Session, username: int):
    return db.query(models.System).\
            filter(models.System.username == username).first()

def update_user(db: Session, user: schemas.User):
    """
    Update an existing user, or create it if missing
    """
    #look for the system in the DB
    _user = get_user(db, user.username)

    #if it exists, update it
    if _user:
        _user.username = user.username
        _user.name = user.name
        _user.userid = user.userid
        _user.email = user.email
        _user.group = user.group
        _user.active = user.active                               
        db.commit()
        db.refresh(_user)
    #otherwise create it
    else:
        _user = models.System(**user.dict())
        db.add(_user)
        #db.commit()
        db.flush()
        db.refresh(_user)
    return _user
