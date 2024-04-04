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

from .utils import log_sync_error, match_project_account_pair

import rimsdash.service.sync.persist as persist

logger = logging.getLogger('rimsdash')


def systems(db: Session = Depends(rdb.get_db)):
    """
    Sync local systems DB to external RIMS DB

    external data will overwrite any local conflicts
    """

    logger.info(f"getting system list from RIMS")
    rims_systems: list[dict] = rims.get_system_list()

    logger.info(f"reading system list into DB")

    for system in rims_systems:
        persist.system(system, db)


def users(db: Session = Depends(rdb.get_db)):
    """
    Sync local user DB to external RIMS DB

    external data will overwrite any local conflicts
    """

    logger.info(f"getting user list from RIMS")
    rims_users: list[dict] = rims.get_user_list()

    logger.info(f"reading user list into DB")
    for user in rims_users:
        persist.user(user, db)

    
def accounts(db: Session = Depends(rdb.get_db)) -> list[dict]:
    """
    Sync local account DB to external RIMS DB
    
    Update projects to include account

    external data will overwrite any local conflicts
    """

    logger.info(f"getting account list from RIMS")
    projectaccount_list: list[dict] = rims.get_project_accounts()
    logger.info(f"reading account list into DB")

    for account in projectaccount_list:
        persist.account(account, db)

    return projectaccount_list



def projects(db: Session = Depends(rdb.get_db)):
    """
    Sync local project DB to external RIMS DB

    external data will overwrite any local conflicts
    """

    logger.info(f"getting project list from RIMS")
    projects: list[dict] = rims.get_project_list()

    logger.info(f"reading project list into DB")
    for project in projects:
        persist.project(project, db)


    logger.info(f"getting additional project details from RIMS")
    project_details: list[dict] = rims.get_project_details()

    logger.info(f"updating DB with additional project details")
    for project in project_details:
        persist.project_details(project, db)

    return projects


def training_requests(db: Session = Depends(rdb.get_db)):
    """
    Sync local request DB to external RIMS DB

    external data will overwrite any local conflicts
    """

    logger.info(f"getting training requests from RIMS")
    training_requests: list[dict] = rims.get_training_request_list()

    logger.info(f"reading request list into DB")

    for trequest in training_requests:
        persist.training_request(trequest, db)

    #get the form ids and associated forms from config
    __form_ids = config.get_csv_list("manual", "training_form_ids", default = [])
    form_ids = list(map(int, __form_ids))
        #FUTURE
        #get this directly from db

    #iterate through known form ids
    for form_id in form_ids:
        trequest_forms: list[dict] = rims.get_trequest_content_list(form_id)

        for trform in trequest_forms:
            persist.training_forms(trform, db)


def project_accounts(project_list: list[dict], projectaccount_list: list[dict], db: Session = Depends(rdb.get_db)):
    """
    Sync project-account pairs to DB

    Iterates through rims-projects and matches to rims-projectaccounts via DB
    """

    logger.info(f"creating projacc")


    for project in project_list:
        #FUTURE: move the below to persist

        try:
            #warn and skip if the account does not exist
            if project['bcode'] == '':
                logger.warn(f"empty bcode {project['bcode']} for project {project['id']}")   

            #if the account is in the DB, find the pair from the local list
            if crud.account.get(db, project['bcode']) is not None:
                project_account = match_project_account_pair(projectaccount_list, project['bcode'], project['id'])

            #else create it with valid = None 
            else:           
                logger.warn(f"account {project['bcode']} not found in DB for project {project['id']}, creating w/ valid=None")
                __account_schema = schemas.account_schema.AccountReceiveSchema(
                    bcode = project['bcode']
                )
                crud.account.create(db, __account_schema)

                project_account = { 
                                   'bcode': project['bcode'], 
                                   'project_id': project['id'], 
                                   'valid': None 
                                   }

            #finally update the db
            persist.project_account(project_account, db)

        except:
            log_sync_error("project", project['id']) 


def user_rights(db: Session = Depends(rdb.get_db)):
    """
    Sync local user rights DB to external RIMS DB

    external data will overwrite any local conflicts
    """

    logger.info(f"Getting user rights from RIMS")

    user_rights_list = rims.get_user_rights_list()

    for user_right in user_rights_list:
        try:
            logger.debug(f"user right for {user_right['username']}")

            #check both system and user exist
            user = crud.user.get(db, user_right['username'])
            if user is None:
                logger.info(f"unrecognised user {user_right['username']} in rims user_rights_list")                     
                continue              

            system = crud.system.get(db, user_right['system_id'])
            if system is None:
                logger.info(f"unrecognised system {user_right['system_id']} for user {user_right['username']}")                     
                continue  

            __schema = schemas.SystemUserReceiveSchema(**user_right)
            __row = crud.systemuser.get(db, (__schema.username, __schema.system_id))

            if __row is None:
                crud.systemuser.create(db, __schema)
            else:
                crud.systemuser.update(db, __row, __schema)
        except:
            log_sync_error("user_right", user_right['username'])



def project_users(db: Session = Depends(rdb.get_db)):
    """
    Sync local project membership DB to external RIMS DB

    external data will overwrite any local conflicts
    """

    logger.info(f"Syncing project rights to RIMS")

    user_projects_list = rims.get_user_projects_list()

    for project_user in user_projects_list:
        try:
            logger.debug(f"project membership for {project_user['username']}")

            #check both user and project exist
            user = crud.user.get(db, project_user['username'])
            if user is None:
                logger.info(f"unrecognised user {project_user['username']} in rims user_projects_list")                     
                continue

            project = crud.project.get(db, project_user['project_id'])
            if project is None:
                logger.info(f"unrecognised system {project_user['project_id']} for user {project_user['username']}")                     
                continue

            __schema = schemas.ProjectUsersReceiveSchema(**project_user)
            __row = crud.projectuser.get(db, (__schema.username, __schema.project_id))

            if __row is None:
                crud.projectuser.create(db, __schema)
            else:
                crud.projectuser.update(db, __row, __schema)
        except:
            log_sync_error("project_user", project_user['username'])