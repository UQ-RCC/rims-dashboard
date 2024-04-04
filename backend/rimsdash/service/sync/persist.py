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
from rimsdash.models.user_models import UserModel

from .utils import log_sync_error, match_project_account_pair

logger = logging.getLogger('rimsdash')


def system(system: dict, db: Session = Depends(rdb.get_db)):
    """
    update system record in DB

    create if not already present
    """

    try:
        system_in = schemas.SystemReceiveSchema(**system)

        __row = crud.system.get(db, system['id'])

        if __row is None:
            logger.debug(f"creating system {system['id']}")

            crud.system.create(db, system_in)

        elif not system_in == schemas.SystemReceiveSchema.from_orm(__row):

            logger.debug(f"updating system {system['id']}")            

            crud.system.update(db, __row, system_in)
        else:
            logger.debug(f"unchanged system {system['id']}")

    except:
        log_sync_error("system", system['id'])



def user(user: dict, db: Session = Depends(rdb.get_db)):
    """
    update user record in DB

    create if not already present
    """

    try:
        user_in = schemas.UserReceiveSchema(**user)

        __row = crud.user.get(db, user['id'])

        if __row is None:
            logger.debug(f"creating user {user['id']}")

            crud.user.create(db, user_in)

        elif not user_in == schemas.UserReceiveSchema.from_orm(__row):

            logger.debug(f"updating user {user['id']}")            

            crud.user.update(db, __row, user_in)
        else:
            logger.debug(f"unchanged user {user['username']}")

    except:
        log_sync_error("user", user['id'])


def account(account: dict, db: Session = Depends(rdb.get_db)) -> list[dict]:
    """
    update account record in DB

    create if not already present
    """

    try:
        __row = crud.account.get(db, account['bcode'])

        account_in = schemas.AccountReceiveSchema(
            bcode = account['bcode'],
        )

        if __row is None:
            logger.debug(f"creating account {account['bcode']}")

            crud.account.create(db, account_in)

        elif not account_in == schemas.AccountReceiveSchema.from_orm(__row):
            logger.debug(f"updating account {account['bcode']}")

            crud.account.update(db, __row, account_in)
        else:
            logger.debug(f"unchanged account {account['bcode']}")            
    except:
        log_sync_error("account", account['bcode'])




def project(project: dict, db: Session = Depends(rdb.get_db)):
    """
    update project record in DB

    create if not already present
    """

    try:
        project_in = schemas.ProjectReceiveSchema(**project)

        __row = crud.project.get(db, project['id'])

        if __row is None:
            logger.debug(f"creating project {project['id']}")

            crud.project.create(db, project_in)

        elif not project_in == schemas.ProjectReceiveSchema.from_orm(__row):

            logger.debug(f"updating project {project['id']}")            

            crud.project.update(db, __row, project_in)
        else:
            logger.debug(f"unchanged project {project['projectname']}")

    except:
        log_sync_error("project", project['id'])



def project_details(project: dict, db: Session = Depends(rdb.get_db)):
    """
    Update project details in DB

    NB: project should already exist before adding details, will not create
    """

    try:
        project_in = schemas.ProjectInitDetailsSchema(**project)

        __row = crud.project.get(db, project['id'])

        if __row is None:
            logger.warn(f"Project {project['id']} found in details report but not present in DB. Project ignored.")    
            pass

        elif not project_in == schemas.ProjectInitDetailsSchema.from_orm(__row):

            logger.debug(f"updating project details {project['id']}")            
            crud.project.update(db, __row, project_in)

        else:
            logger.debug(f"unchanged project details: {project['projectname']}")

    except:
        log_sync_error("project", project['id'])


def training_request(trequest: dict, db: Session = Depends(rdb.get_db)):
    """
    update training_request record in DB

    create if not already present
    """

    try:

        #fetch username from request uid
        __user = crud.user.get_by_userid(db, userid=trequest['user_id'])

        if __user is not None:
            
            #add the username and create the schema
            trequest['username'] = __user.username

            trequest_in = schemas.TrainingRequestReceiveSchema.parse_obj(trequest)

            __row = crud.trequest.get(db, trequest['id'])

            if __row is None:
                logger.debug(f"creating request {trequest['id']} for user {trequest['username']}")

                crud.trequest.create(db, trequest_in)

            elif not trequest_in == schemas.TrainingRequestReceiveSchema.from_orm(__row):

                logger.debug(f"updating request {trequest['id']} for user {trequest['username']}")

                crud.trequest.update(db, __row, trequest_in)
            else:
                logger.debug(f"unchanged training_request {trequest['id']}")            
        else:
            logger.warn(f"RIMS uid {trequest['user_id']} from training request  {trequest['id']} not found in local DB")
            pass

    except:
        log_sync_error("trequest", trequest['user_id'])



def training_forms(trform: dict, db: Session = Depends(rdb.get_db)):
    """
    add form data blob to training request in DB

    NB: trequest must exist
    """

    try:
        row = crud.trequest.get(db, trform['id'])

        trequest_in = schemas.TrainingRequestAddFormDataSchema.parse_obj(trform)

        if row is None:
            logger.error(f"request {trform['id']} for user {trform['user_fullname']} not found in DB")
            pass

        elif not trequest_in == schemas.TrainingRequestAddFormDataSchema.from_orm(row):
            logger.debug(f"adding form data to {trform['id']} for user {row.username}")

            crud.trequest.update(db, row, trequest_in)
        else:
            logger.debug(f"unchanged trform {trform['id']}")                

    except:
        log_sync_error("trform", trform['id']) 


def project_account( project_account, db):
    try:
        projacc_in = schemas.ProjectAccountReceiveSchema(
            bcode = project_account['bcode'],
            project_id = project_account['id'],
            valid = project_account['valid'],
        )

        __row = crud.projectaccount.get(db, (project_account['bcode'], project_account['id']) )

        if __row is None:
            logger.debug(f"creating projectaccount {project_account['bcode']} for project {project_account['id']}")
            crud.projectaccount.create(db, projacc_in)
        elif not projacc_in == schemas.ProjectAccountReceiveSchema.from_orm(__row):
            logger.debug(f"updating projectaccount {project_account['bcode']} for project {project_account['id']}")        
            crud.projectaccount.update(db, __row, projacc_in)
        else:
            logger.debug(f"no updates for projectaccount {project_account['bcode']}, project {project_account['id']}")
            pass
    except:
        log_sync_error("project_account", project_account['id']) 



def admin_user(user_row: UserModel, admin_dict: dict, db: Session = Depends(rdb.get_db), skip_existing: bool = False):
    """
    Sync admin status in DB to external RIMS DB

    NB: input is DB row, not dict/schema
    """

    try:
        if user_row is not None:
            if skip_existing and user_row.admin == False:
                logger.debug(f"admin sync: skip non-admin {user_row.username}")
            else:
                logger.debug(f"admin sync: {user_row.username}")

                user_admin_in = schemas.user_schema.UserUpdateAdminSchema(**admin_dict)

                crud.user.update(db, user_row, user_admin_in)
    except:
        log_sync_error("user admin status", user_row.username)