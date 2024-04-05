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


def process_projects(db: Session = Depends(rdb.get_db)):
    """
    Calculate status for projects
    """

    projects = crud.project.get_all(db)

    for project in projects:
        try:
            project_schema = schemas.ProjectForStateCheckSchema.from_orm(project)

            project_state: schemas.ProjectStateInitSchema = logic.process_project(project_schema)

            _row = crud.project_state.get(db, project.id)

            if _row is None:
                logger.debug(f'writing state for project {project.id}')                    
                project_state = schemas.ProjectStateInitSchema.validate(project_state)
                crud.project_state.create(db, project_state)

            elif not schemas.ProjectStateProcessSchema.validate(project_state) \
                    == schemas.ProjectStateProcessSchema.from_orm(_row):

                logger.debug(f'updating state for project {project.id}')                  
                project_state = schemas.ProjectStateInitSchema.validate(project_state)
                crud.project_state.update(db, _row, project_state)

            else:
                logger.debug(f'unchanged state for project {project.id}')                  
                pass
        except:
            log_sync_error("project state", project.id)

def process_users(db: Session = Depends(rdb.get_db)):
    """
    calculate status for users
    """
    users = crud.user.get_all(db)

    for user in users:
        try:
            user_schema = schemas.UserForStateCheckSchema.from_orm(user)

            user_state: schemas.UserStateInitSchema = logic.process_user(user_schema)

            _row = crud.user_state.get(db, user.username)

            if _row is None:
                logger.debug(f'writing state for user {user.username}')                 
                user_state = schemas.UserStateInitSchema.validate(user_state)
                crud.user_state.create(db, user_state)

            elif not schemas.UserStateProcessSchema.validate(user_state) \
                    == schemas.UserStateProcessSchema.from_orm(_row):

                logger.debug(f'updating state for user {user.username}') 
                user_state = schemas.UserStateInitSchema.validate(user_state)
                crud.user_state.update(db, _row, user_state)

            else:
                logger.debug(f'unchanged state for user {user.username}')                 
                pass
        except:
            log_sync_error("user state", user.username)

def postprocess_projects(db: Session = Depends(rdb.get_db)):
    
    projects = crud.project.get_all(db)

    for project in projects:
        try:
            project_schema = schemas.ProjectOutRefsSchema.from_orm(project)

            project_state_updated: schemas.ProjectStatePostProcessUpdateSchema \
                    = logic.postprocess_project(project_schema)
            
            project_state = schemas.ProjectStatePostProcessUpdateSchema.validate(project_state_updated)
            
            _row = crud.project_state.get(db, project.id)

            if _row is None:
                logger.warn(f'project-state {project.id} not found in database during postprocessing')

            elif not project_state == schemas.ProjectStatePostProcessUpdateSchema.from_orm(_row):
                logger.debug(f'writing post-state for project {project.id}')                
                crud.project_state.update(db, _row, project_state)

            else:
                logger.debug(f'unchanged post-state for project {project.id}')                    
                pass
        except:
            log_sync_error("project post-state", project.id)

def postprocess_users(db: Session = Depends(rdb.get_db)):
    
    users = crud.user.get_all(db)

    for user in users:
        try:
            user_schema = schemas.UserOutRefsSchema.from_orm(user)

            user_state_updated = logic.postprocess_user(user_schema)
            user_state = schemas.UserStatePostProcessUpdateSchema.validate(user_state_updated)

            _row = crud.user_state.get(db, user.username)

            if _row is None:
                logger.warn(f'user-state {user.username} not found in database after update')

            elif not user_state == schemas.UserStatePostProcessUpdateSchema.from_orm(_row):
                logger.debug(f'writing post-state for user {user.username}')
                crud.project_state.update(db, _row, user_state)

            else:
                logger.debug(f'unchanged post-state for user {user.username}')                
                pass
        except:
            log_sync_error("user post-state", user.username)


def process_trequests(db: Session = Depends(rdb.get_db)):
    
    trequests = crud.trequest.get_all(db)

    for trequest in trequests:
        try:

            trequest_schema = schemas.TrainingRequestForProcessingSchema.from_orm(trequest)

            trequest_updated: schemas.TrainingRequestUpdateStateSchema \
                = logic.process_trequest(trequest_schema)

            _row = crud.trequest.get(db, trequest.id)

            if _row is None:
                logger.warn(f'training request {trequest.id} absent in DB on attempted update')

            elif not trequest_updated == schemas.TrainingRequestUpdateStateSchema.from_orm(_row):
                logger.debug(f'updating state for trequest  {trequest.id}')
                crud.trequest.update(db, _row, trequest_updated)

            else:
                logger.debug(f'unchanged state for trequest  {trequest.id}')
                pass
        except:
            log_sync_error("trequest state", trequest.id)