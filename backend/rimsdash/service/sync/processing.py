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
import rimsdash.service.logic as logic

from rimsdash.models import SystemRight, ProjectRight, SyncType

from .utils import log_sync_error

logger = logging.getLogger('rimsdash')

#sessionmaker = FastAPISessionMaker(SQLALCHEMY_DATABASE_URL)

ACCEPTED_REALMS = {'admin', 'dashboard'}


def process_projects(db: Session = Depends(rdb.get_db)):
    """
    Calculate status for projects
    """

    projects = crud.project.get_all(db)

    for project in projects:
        try:
            logger.debug(f"project state: {project.id}")
            project_schema = schemas.ProjectForStateCheckSchema.from_orm(project)

            project_state = logic.process_project(project_schema)

            _row = crud.project_state.get(db, project.id)

            #FUTURE: need to sort out create vs update, much simpler if can unify
            if _row is None:
                project_state = schemas.ProjectStateReceiveSchema.validate(project_state)
                crud.project_state.create(db, project_state)
            else:
                project_state = schemas.ProjectStateUpdateSchema.validate(project_state)
                crud.project_state.update(db, _row, project_state)
        except:
            log_sync_error("project state", project.id)

def process_users(db: Session = Depends(rdb.get_db)):
    """
    calculate status for users
    """
    users = crud.user.get_all(db)

    for user in users:
        try:
            logger.debug(f"user state: {user.username}")
            user_schema = schemas.UserForStateCheckSchema.from_orm(user)

            user_state = logic.process_user(user_schema)

            _row = crud.user_state.get(db, user.username)

            #FUTURE: need to sort out create vs update, much simpler if can unify
            if _row is None:
                user_state = schemas.UserStateReceiveSchema.validate(user_state)
                crud.user_state.create(db, user_state)
            else:
                user_state = schemas.UserStateUpdateSchema.validate(user_state)
                crud.user_state.update(db, _row, user_state)
        except:
            log_sync_error("user state", user.username)

def postprocess_projects(db: Session = Depends(rdb.get_db)):
    
    projects = crud.project.get_all(db)

    for project in projects:
        try:
            logger.debug(f'posprocessing proj {project.id}')
            project_schema = schemas.ProjectOutRefsSchema.from_orm(project)

            project_state_updated = logic.postprocess_project(project_schema)

            _row = crud.project_state.get(db, project.id)

            if _row is not None:
                project_state = schemas.ProjectStatePostProcessUpdateSchema.validate(project_state_updated)
                crud.project_state.update(db, _row, project_state)
            else:
                logger.warn(f'project-state {project.id} not found in database after update')
        except:
            log_sync_error("project post-state", project.id)

def postprocess_users(db: Session = Depends(rdb.get_db)):
    
    users = crud.user.get_all(db)

    for user in users:
        try:
            logger.debug(f'posprocessing user {user.username}')
            user_schema = schemas.UserOutRefsSchema.from_orm(user)

            user_state_updated = logic.postprocess_user(user_schema)

            _row = crud.user_state.get(db, user.username)

            if _row is not None:
                user_state = schemas.UserStatePostProcessUpdateSchema.validate(user_state_updated)
                crud.project_state.update(db, _row, user_state)
            else:
                logger.warn(f'user-state {user.username} not found in database after update')
        except:
            log_sync_error("user post-state", user.username)

def process_trequests(db: Session = Depends(rdb.get_db)):
    
    trequests = crud.trequest.get_all(db)

    for trequest in trequests:
        try:
            logger.debug(f'posprocessing training request  {trequest.id}')
            trequest_schema = schemas.TrainingRequestForProcessingSchema.from_orm(trequest)

            trequest_updated: schemas.TrainingRequestUpdateStateSchema \
                = logic.process_trequest(trequest_schema)

            _row = crud.trequest.get(db, trequest.id)

            if _row is not None:
                crud.trequest.update(db, _row, trequest_updated)
            else:
                logger.warn(f'training request {trequest.id} absent in DB on attempted update')
        except:
            log_sync_error("trequest state", trequest.id)