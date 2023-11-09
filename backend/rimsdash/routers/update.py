import logging

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi_utils.session import FastAPISessionMaker

import rimsdash.config as config
import rimsdash.db as rdb
import rimsdash.external as external
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

def sync_systems(db: Session = Depends(rdb.get_db)):
    """
    Sync local systems DB to external RIMS DB

    external data will overwrite any local conflicts
    """

    logger.info(f"getting system list from RIMS")
    systems = external.rims.get_system_list()

    logger.info(f"reading system list into DB")
    for system in systems:

        _row = crud.system.get(db, system['id'])

        if _row is None:
            logger.debug(f"creating {system['id']}")
            system_in = schemas.SystemCreateSchema(**system)

            crud.system.create(db, system_in)
        else:
            logger.debug(f"updating {system['id']}")            
            system_in = schemas.SystemCreateSchema(**system)

            crud.system.update(db, _row, system_in)


def sync_users(db: Session = Depends(rdb.get_db)):
    """
    Sync local user DB to external RIMS DB

    external data will overwrite any local conflicts
    """

    logger.info(f"getting user list from RIMS")
    users = external.rims.get_user_list()

    logger.info(f"reading user list into DB")
    for user in users:

        _row = crud.user.get(db, user['username'])

        if _row is None:
            logger.debug(f"creating {user['username']}")
            user_in = schemas.UserCreateSchema(**user)

            crud.user.create(db, user_in)
        else:
            logger.debug(f"updating {user['username']}")            
            user_in = schemas.UserCreateSchema(**user)

            crud.user.update(db, _row, user_in)



def sync_projects(db: Session = Depends(rdb.get_db)):
    """
    Sync local project DB to external RIMS DB

    external data will overwrite any local conflicts
    """

    logger.info(f"getting project list from RIMS")
    projects = external.rims.get_project_list()

    logger.info(f"reading project list into DB")
    for project in projects:

        _row = crud.project.get(db, project['id'])

        if _row is None:
            logger.debug(f"creating {project['id']}")
            project_in = schemas.ProjectCreateSchema(**project)

            crud.project.create(db, project_in)
        else:
            logger.debug(f"updating {project['id']}")            
            project_in = schemas.ProjectCreateSchema(**project)

            crud.project.update(db, _row, project_in)

    logger.info(f"getting additional project details from RIMS")
    project_details = external.rims.get_project_details()

    logger.info(f"updating DB with additional project details")
    for project in project_details:

        _row = crud.project.get(db, project['id'])

        if _row is None:
            logger.error(f"project {project['id']} from details report not found in DB")
            pass
        else:
            logger.debug(f"updating {project['id']}")   
            project_in = schemas.ProjectInitDetailsSchema(**project)

            crud.project.update(db, _row, project_in)

def get_session():
    with sessionmaker.context_session() as db:
        return db

def run_sync():
    """
    perform primary sync
    """
    logger.info("starting DB update")

    with sessionmaker.context_session() as db:
        sync_systems(db)
        sync_users(db)
        sync_projects(db)
        return db
