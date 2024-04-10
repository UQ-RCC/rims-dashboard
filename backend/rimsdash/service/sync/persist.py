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

from rimsdash.models import SystemRight, ProjectRight, SyncType, AdminRight
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

        __row = crud.user.get(db, user['username'])

        if __row is None:
            logger.debug(f"creating user {user['username']}")

            crud.user.create(db, user_in)

        elif not user_in == schemas.UserReceiveSchema.from_orm(__row):

            logger.debug(f"updating user {user['username']}")            

            crud.user.update(db, __row, user_in)
        else:
            logger.debug(f"unchanged user {user['username']}")

    except:
        log_sync_error("user", user['username'])


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
            logger.debug(f"unchanged project {project['id']}")

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
            logger.debug(f"unchanged project details: {project['id']}")

    except:
        log_sync_error("project", project['id'])


def project_account( project_account: dict, db: Session = Depends(rdb.get_db)):
    """
    update project_account association in DB

    create if not already present
    """    
    try:
        projacc_in = schemas.ProjectAccountReceiveSchema(
            bcode = project_account['bcode'],
            project_id = project_account['project_id'],
            valid = project_account['valid'],
        )

        __row = crud.projectaccount.get(db, (project_account['bcode'], project_account['project_id']) )

        if __row is None:
            logger.debug(f"creating projectaccount {project_account['bcode']} for project {project_account['project_id']}")
            crud.projectaccount.create(db, projacc_in)
        elif not projacc_in == schemas.ProjectAccountReceiveSchema.from_orm(__row):
            logger.debug(f"updating projectaccount {project_account['bcode']} for project {project_account['project_id']}")        
            crud.projectaccount.update(db, __row, projacc_in)
        else:
            logger.debug(f"no updates for projectaccount {project_account['bcode']}, project {project_account['project_id']}")
            pass
    except:
        log_sync_error("project_account", project_account['project_id']) 



def admin_user(user_row: UserModel, db: Session = Depends(rdb.get_db), skip_existing: bool = False):
    """
    Sync admin status in DB to external RIMS DB

    NB: input is DB row, not dict/schema
    """

    try:
        if skip_existing and user_row.admin in [ AdminRight.user, AdminRight.previous ]  :
            logger.debug(f"admin sync: skip {user_row.username}, existing rights: {user_row.admin} ")
        else:

            try:
                admin_dict = rims.get_admin_status(user_row.username)
            except: 
                log_sync_error("rims admin status", user_row.username)

            user_admin_in = schemas.user_schema.UserUpdateAdminSchema(**admin_dict)

            logger.debug(f"admin sync: updating {user_row.username}, rights: {user_admin_in.admin}")

            crud.user.update(db, user_row, user_admin_in)
    except:
        log_sync_error("user admin status", user_row.username)


def user_right(user_right: dict, db: Session = Depends(rdb.get_db)):
    """
    update instrument user_right association in DB

    create if not already present
    """          
    try:

        #check both system and user exist
        user = crud.user.get(db, user_right['username'])

        if user is None:
            logger.info(f"unrecognised user {user_right['username']} in rims user_rights_list")                     
            return              

        system = crud.system.get(db, user_right['system_id'])
        if system is None:
            logger.info(f"unrecognised system {user_right['system_id']} for user {user_right['username']}")                     
            return  

        __schema = schemas.SystemUserReceiveSchema(**user_right)
        __row = crud.systemuser.get(db, (__schema.username, __schema.system_id))

        if __row is None:
            logger.debug(f"creating systemuser {__schema.username} : {__schema.system_id}")                
            crud.systemuser.create(db, __schema)
        elif not __schema == schemas.SystemUserReceiveSchema.from_orm(__row):
            logger.debug(f"PRE {__row.username} : {__row.system_id}, {__row.status}")  
            logger.debug(f"NEW {__schema.username} : {__schema.system_id}, {__schema.status}")                  
            crud.systemuser.update(db, __row, __schema)
            logger.debug(f"POST {__row.username} : {__row.system_id}, {__row.status}")
            #__debug = crud.systemuser.get(db, (__schema.username, __schema.system_id))
            #logger.debug(f"FETCH {__debug.username} : {__debug.system_id}, {__debug.status}")
        else:
            logger.debug(f"unchanged systemuser {__schema.username} : {__schema.system_id}")                    
    except:
        log_sync_error("systemuser", user_right['username'])


def project_user(project_user: dict, db: Session = Depends(rdb.get_db)):
    """
    update project_user right association in DB

    create if not already present
    """
    try:

        #check both user and project exist
        user = crud.user.get(db, project_user['username'])

        if user is None:
            logger.info(f"unrecognised user {project_user['username']} in rims user_projects_list")                     
            return

        project = crud.project.get(db, project_user['project_id'])
        if project is None:
            logger.info(f"unrecognised system {project_user['project_id']} for user {project_user['username']}")                     
            return

        __schema = schemas.ProjectUsersReceiveSchema(**project_user)
        __row = crud.projectuser.get(db, (__schema.username, __schema.project_id))


        if __row is None:
            logger.debug(f"creating projectuser {__schema.username} : {__schema.project_id}")                
            crud.projectuser.create(db, __schema)
        elif not __schema == schemas.ProjectUsersReceiveSchema.from_orm(__row):
            logger.debug(f"updating projectuser {__schema.username} : {__schema.project_id}")                  
            crud.projectuser.update(db, __row, __schema)
        else:
            logger.debug(f"unchanged projectuser {__schema.username} : {__schema.project_id}") 

    except:
        log_sync_error("project_user", project_user['username'])    


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

            trequest_in = schemas.TrainingRequestCreateSchema.parse_obj(trequest)

            __row = crud.trequest.get(db, trequest['id'])

            if __row is None:
                logger.debug(f"creating request {trequest['id']} for user {trequest['username']}")

                crud.trequest.create(db, trequest_in)

            elif not trequest_in == schemas.TrainingRequestCreateSchema.from_orm(__row):

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