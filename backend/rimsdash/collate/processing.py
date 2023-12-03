import logging
import datetime

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi_utils.session import FastAPISessionMaker

import rimsdash.config as config
import rimsdash.db as rdb
import rimsdash.external.rims as rims
import rimsdash.schemas as schemas
import rimsdash.crud as crud
import rimsdash.collate.logic as logic

from rimsdash.models import SystemRight, ProjectRight, SyncType

logger = logging.getLogger('rimsdash')

#sessionmaker = FastAPISessionMaker(SQLALCHEMY_DATABASE_URL)

def sync_systems(db: Session = Depends(rdb.get_db)):
    """
    Sync local systems DB to external RIMS DB

    external data will overwrite any local conflicts
    """

    logger.info(f"getting system list from RIMS")
    systems: list[dict] = rims.get_system_list()

    logger.info(f"reading system list into DB")
    for system in systems:

        __row = crud.system.get(db, system['id'])

        if __row is None:
            logger.debug(f"creating {system['id']}")
            system_in = schemas.SystemCreateSchema(**system)

            crud.system.create(db, system_in)
        else:
            logger.debug(f"updating {system['id']}")            
            system_in = schemas.SystemCreateSchema(**system)

            crud.system.update(db, __row, system_in)


def sync_users(db: Session = Depends(rdb.get_db)):
    """
    Sync local user DB to external RIMS DB

    external data will overwrite any local conflicts
    """

    logger.info(f"getting user list from RIMS")
    users: list[dict] = rims.get_user_list()

    logger.info(f"reading user list into DB")
    for user in users:

        __row = crud.user.get(db, user['username'])

        if __row is None:
            logger.debug(f"creating user {user['username']}")
            user_in = schemas.UserCreateSchema(**user)

            crud.user.create(db, user_in)
        else:
            logger.debug(f"updating user {user['username']}")            
            user_in = schemas.UserUpdateSchema(**user)

            crud.user.update(db, __row, user_in)


def sync_user_admin(db: Session = Depends(rdb.get_db), skip_existing: bool = False):
    """
    Sync admin status in DB to external RIMS DB
    """
    logger.info(f"Syncing admin status")
    for __row in crud.user.get_all(db):
        if __row is not None:
            if skip_existing and __row.admin is not None:
                pass
            else:
                logger.debug(f"admin sync: {__row.username}")
                __admin = rims.get_admin_status(__row.username)

                user_admin_in = schemas.user_schema.UserUpdateAdminSchema(admin=__admin)

                crud.user.update(db, __row, user_admin_in)



def sync_projects(db: Session = Depends(rdb.get_db)):
    """
    Sync local project DB to external RIMS DB

    external data will overwrite any local conflicts
    """

    logger.info(f"getting project list from RIMS")
    projects: list[dict] = rims.get_project_list()

    logger.info(f"reading project list into DB")
    for project in projects:

        _row = crud.project.get(db, project['id'])

        if _row is None:
            logger.debug(f"creating project {project['id']}")
            project_in = schemas.ProjectCreateSchema(**project)

            crud.project.create(db, project_in)
        else:
            logger.debug(f"updating project {project['id']}")            
            project_in = schemas.ProjectCreateSchema(**project)

            crud.project.update(db, _row, project_in)

    logger.info(f"getting additional project details from RIMS")
    project_details: list[dict] = rims.get_project_details()

    logger.info(f"updating DB with additional project details")
    for project in project_details:

        _row = crud.project.get(db, project['id'])

        if _row is None:
            logger.warn(f"Project {project['id']} found in RIMS details report but not present in DB. Project ignored.")
            pass
        else:
            logger.debug(f"Updating project {project['id']}")   
            project_in = schemas.ProjectInitDetailsSchema(**project)

            crud.project.update(db, _row, project_in)

def sync_user_rights(db: Session = Depends(rdb.get_db)):
    """
    Sync local user rights DB to external RIMS DB

    external data will overwrite any local conflicts
    """
    
    logger.info(f"Syncing user rights to RIMS")

    users = crud.user.get_all(db)
    
    #DEBUG
    _cutoff = 99999
    _counter = 0

    for user in users:
        if _counter >= _cutoff: #debug
            break

        logger.debug(f"sync rights {user.username}")
        rights_dict = rims.queries.get_user_rights(user.username)

        for key in rights_dict:
            __schema = schemas.SystemUserCreateSchema(username=user.username, system_id=key, status=SystemRight(rights_dict[key]))

            __row = crud.systemuser.get(db, (user.username, key))
            __system = crud.system.get(db, key)

            #check system exists - report includes systems from other cores            
            if __system is not None:

                if __row is None:
                    crud.systemuser.create(db, __schema)
                else:
                    crud.systemuser.update(db, __row, __schema)
            else:
                logger.debug(f"unrecognised rights for user {user.username} on system {key}")    
        
        _counter+=1 #debug





def sync_project_users(db: Session = Depends(rdb.get_db)):
    """
    Sync local project users DB to external RIMS DB

    external data will overwrite any local conflicts
    """
    
    logger.info(f"syncing project users to RIMS")

    projects = crud.project.get_all(db)

    #DEBUG
    _cutoff = 99999
    _counter = 0

    for project in projects:
        if _counter >= _cutoff: #debug
            break

        logger.debug(f"sync project users {project.id}")
        username_list = rims.queries.get_project_users(project.id)

        for username in username_list:
            __schema = schemas.ProjectUsersBaseSchema(username=username, project_id=project.id, status=ProjectRight("M"))

            __row = crud.projectusers_rights.get(db, (username, project.id))

            if __row is None:
                crud.projectusers_rights.create(db, __schema)
            else:
                crud.projectusers_rights.update(db, __row, __schema)
 
        _counter+=1 #debug

def process_projects(db: Session = Depends(rdb.get_db)):
    """
    Calculate status for projects
    """

    projects = crud.project.get_all(db)

    for project in projects:
        logger.debug(f"project state: {project.id}")
        project_schema = schemas.ProjectFullSchema.validate(project)

        project_state = logic.process_project(project_schema)

        _row = crud.project_state.get(db, project.id)

        #FUTURE: need to sort out create vs update, much simpler if can unify
        if _row is None:
            project_state = schemas.ProjectStateCreateSchema.validate(project_state)
            crud.project_state.create(db, project_state)
        else:
            project_state = schemas.ProjectStateUpdateSchema.validate(project_state)
            crud.project_state.update(db, _row, project_state)

def process_users(db: Session = Depends(rdb.get_db)):
    """
    calculate status for users
    """
    users = crud.user.get_all(db)

    for user in users:
        logger.debug(f"user state: {user.username}")
        user_schema = schemas.UserFullSchema.validate(user)

        user_state = logic.process_user(user_schema)

        _row = crud.user_state.get(db, user.username)

        #FUTURE: need to sort out create vs update, much simpler if can unify
        if _row is None:
            user_state = schemas.UserStateCreateSchema.validate(user_state)
            crud.user_state.create(db, user_state)
        else:
            user_state = schemas.UserStateUpdateSchema.validate(user_state)
            crud.user_state.update(db, _row, user_state)



def calc_states(db):
    """
    recalculate states only
    """
    logger.info(">>>>>>>>>>>> Begin calculating states")
    process_projects(db)
    process_users(db)
    logger.info(">>>>>>>>>>>> Finished calculating states")


def primary_sync(db: Session = Depends(rdb.get_db), force=False):
        """
        perform full sync

        WARNING: many RIMS API calls (6k+)
            to be reduced by new reports when available
        """
        sync_frequency = int(config.get('sync', 'full_sync_frequency'))

        try:
            __last = crud.sync.get_latest_completion(db)
        except:
            __last = None

        if force or __last is None or (datetime.datetime.now() - __last.start_time  > datetime.timedelta(days=sync_frequency)):
            logger.info(">>>>>>>>>>>> Begin full sync")
            __start_schema = schemas.sync_schema.SyncCreateSchema(sync_type=SyncType.full)
            __current = crud.sync.create(db, __start_schema)

            try:
                logger.info(">>>>>>>>>>>> Begin syncing to RIMS")
                sync_systems(db)
                sync_users(db)
                sync_projects(db)
                sync_user_rights(db)
                sync_project_users(db)
                sync_user_admin(db, skip_existing = True)
                logger.info(">>>>>>>>>>>> Finished syncing to RIMS")

                logger.info(">>>>>>>>>>>> Begin calculating states")
                process_projects(db)
                process_users(db)
                logger.info(">>>>>>>>>>>> Finished calculating states")
                __complete_schema = schemas.sync_schema.SyncCompleteSchema(id=__current.id, sync_type=__current.sync_type)
                __updated = crud.sync.update(db, __current, __complete_schema)
                logger.info(">>>>>>>>>>>> Completed full sync")
            except:
                logger.error("!!!!! ERROR: Sync not completed")
                __complete_schema = schemas.sync_schema.SyncCompleteSchema(id=__current.id, sync_type=__current.sync_type, complete=False)
                __updated = crud.sync.update(db, __current, __complete_schema)
        else:
            logger.warn(">>>>>>>>>>>> Sync not attempted, time difference less than sync frequency")
