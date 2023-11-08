import logging

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi_utils.session import FastAPISessionMaker

import rimsdash.config as config
import rimsdash.db as rdb
import rimsdash.rims as rims
import rimsdash.schemas as schemas
import rimsdash.crud as crud

SQLALCHEMY_DATABASE_URL = (f"{config.get('database', 'type')}://"
                           f"{config.get('database', 'db_username')}:"
                           f"{config.get('database', 'db_password')}@"
                           f"{config.get('database', 'host')}:"
                           f"{config.get('database', 'port')}/"
                           f"{config.get('database', 'db_name')}")

logger = logging.getLogger('rimsdash')

sessionmaker = FastAPISessionMaker(SQLALCHEMY_DATABASE_URL)

def update_systems(db: Session = Depends(rdb.get_db)):

    systems = rims.get_systems()

    for system in systems:

        _row = crud.system.get(db, system['id'])

        if _row is None:
            logger.debug(f"creating {system['id']}")
            system_in = schemas.SystemCreateSchema(**system,
            )

            crud.system.create(db, system_in)
        else:
            logger.debug(f"updating {system['id']}")            
            system_in = schemas.SystemUpdateSchema(**system
            )

            crud.system.update(db, _row, system_in)


def update_users(db: Session = Depends(rdb.get_db)):
    users = rims.get_userlist()

    for user in users:
        user_in = schemas.UserCreateSchema(**user
        )
        crud.user.create(db, user_in)
        

def update_projects(db: Session = Depends(rdb.get_db)):
    projects = rims.get_projects()

    for project in projects:
        project_in = schemas.UserCreateSchema(**project
        )
        crud.user.create(db, project_in)

def run_sync():
    logger.info("starting DB update")

    with sessionmaker.context_session() as db:
        update_systems(db)
        return db
