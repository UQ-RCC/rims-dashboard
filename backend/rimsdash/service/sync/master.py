
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

import rimsdash.service.sync.batch as batch
import rimsdash.service.sync.processing as processing
import rimsdash.service.sync.sequential as sequential

logger = logging.getLogger('rimsdash')

def rims_sync_batch_lists(db):
    """
    sync batchable report data only

    NB: fairly quick
    """    
    logger.info(">>>>>>>>>>>> Begin syncing batch data from RIMS")
    batch.systems(db)
    batch.users(db)

    #   FUTURE refactor these 
    project_list = batch.projects(db)
    projectaccount_list = batch.accounts(db)
    batch.project_accounts(project_list, projectaccount_list, db)
    #   /end refactor target

    batch.user_rights(db)
    batch.project_users(db)
    batch.training_requests(db)

    logger.info(">>>>>>>>>>>> Finished syncing batch data from RIMS")


def rims_sync_individual(db, skip_existing = True):
    """
    sync additional data requiring individual calls

    NB: slow!
    """
    logger.info(">>>>>>>>>>>> Begin syncing individual data from RIMS")
    sequential.admin_users(db, skip_existing = True)
    logger.info(">>>>>>>>>>>> Finished syncing individual data from RIMS")


def calc_states(db):
    """
    recalculate states only
    """
    logger.info(">>>>>>>>>>>> Begin calculating states")
    processing.process_projects(db)
    processing.process_users(db)
    processing.postprocess_projects(db)
    processing.postprocess_users(db)
    processing.process_trequests(db) 
    logger.info(">>>>>>>>>>>> Finished calculating states")

def dummy_sync(db, sync_type: SyncType = SyncType.update):
    """
    add dummy sync to DB
    """
    logger.info(">>>>>>>>>>>> DEV adding fake sync to DB")
    #FUTURE: add a dummy sync type to models/base_model
    __start_schema = schemas.SyncCreateSchema(sync_type=sync_type)
    __current = crud.sync.create(db, __start_schema)

    __complete_schema = schemas.SyncCompleteSchema(id=__current.id, sync_type=__current.sync_type)
    __updated = crud.sync.update(db, __current, __complete_schema)

    __last = crud.sync.get_latest_completion(db)
    logger.info(">>>>>>>>>>>> DEV finished adding fake sync to DB")


def remake_db(db: Session = Depends(rdb.get_db), force=False):
    if force == True:
        rdb.drop_db(force=True)

        rdb.init_db()    

        new_db = rdb.get_session()

    return new_db


def primary_sync(db: Session = Depends(rdb.get_db), force=False):
    """
    perform full sync

    DEPRECATED
    """

    if config.get('sync', 'recreate_db', default=True) == "True":
        remake = True
    else:
        remake = False

    if remake:
        logger.info("!!!!wipe and recreate DB")
        db = remake_db(db, force=remake)
    
    sync_frequency_days = int(config.get('sync', 'full_sync_frequency', default=1))

    try:
        __last = crud.sync.get_latest_completion(db)
    except:
        __last = None

            #FUTURE update the time delta here to allow sync at -5 min

    try:
        time_since_sync = datetime.datetime.now() - __last.start_time       
    except:
        time_since_sync = datetime.timedelta(seconds=1)
        
    delta = datetime.timedelta(days=sync_frequency_days) - datetime.timedelta(minutes=5)

    if force or __last is None or (time_since_sync  >= delta):
        logger.info(">>>>>>>>>>>> Begin full sync")
        __start_schema = schemas.sync_schema.SyncCreateSchema(sync_type=SyncType.full)
        __current = crud.sync.create(db, __start_schema)

        try:
            rims_sync_batch_lists(db)

            if True:
                rims_sync_individual(db)
            calc_states(db)

            __complete_schema = schemas.sync_schema.SyncCompleteSchema(id=__current.id, sync_type=__current.sync_type)
            __updated = crud.sync.update(db, __current, __complete_schema)
            logger.info(">>>>>>>>>>>> Completed full sync")
        except:
            logger.error("!!!!! ERROR: Sync not completed", exc_info=True)
            __complete_schema = schemas.sync_schema.SyncCompleteSchema(id=__current.id, sync_type=__current.sync_type, complete=False)
            __updated = crud.sync.update(db, __current, __complete_schema)
    else:
        logger.warn(">>>>>>>>>>>> Sync not attempted, time difference less than sync frequency")


"""
managing accounts/projects is a bit complex

sync_accounts to populate just the accounts with bcodes

sync_projects to populate projects
    likely needs to look up accounts db to properly populate join table
    if projectaccount does not exist
        assign valid = False
    else:
        valid = row.valid

now update_accounts to assign validity to all project accounts
    any weirdness will show here, so maybe check consistency

"""

"""
FUTURE: refactor project_list, projectaccount_list to reduce passing of secondary lists above

pseudo:

#empty projectaccounts table?

def sync_projects                
    for project in projects
        if crud.account.get(db, bcode) is None:
            __aschema = schemas.xxx.(bcode = bcode)
            crud.account.create(db, __aschema)
        if crud.projectaccount.get(db, bcode, project_id) is None:
            __paschema = schemas.xxx.(..., valid = None)
            crud.projectaccount.create(db, __paschema)
    
palist = rims.getxxxx

def match_projectaccounts:
    for pa in palist:
        if crud.projectaccount.get(db, bcode, project_id):
            __paschema( valid = pa['valid'])
            crud.projectaccount.update(db, __paschema)

"""
