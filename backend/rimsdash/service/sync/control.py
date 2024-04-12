
import logging
import datetime
from time import sleep

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi_utils.session import FastAPISessionMaker

import rimsdash.config as config
import rimsdash.db as rdb
import rimsdash.external.rims as rims
import rimsdash.schemas as schemas
import rimsdash.crud as crud
import rimsdash.service.logic as logic

from rimsdash.models import SystemRight, ProjectRight, SyncType, SyncStatus

from .utils import log_sync_error

import rimsdash.service.access as access

import rimsdash.service.sync.batch as batch
import rimsdash.service.sync.processing as processing
import rimsdash.service.sync.sequential as sequential
import rimsdash.service.sync.master as master

logger = logging.getLogger('rimsdash')

SYNC_WAIT_FULL_DAYS = int(config.get('sync', 'sync_wait_full_days', default=7))
SYNC_WAIT_FULL_GRACE = 12   #hours

SYNC_WAIT_MINOR_HOURS = int(config.get('sync', 'sync_wait_minor_hours', default=6))
SYNC_WAIT_MINOR_GRACE = 1   #hours

def remake_db(db: Session = Depends(rdb.get_db), force=False):
    if force == True:
        logger.debug(">>>>>>>>>>>> dropping DB")
        rdb.drop_db(force=True)
        sleep(5)
        logger.debug(">>>>>>>>>>>> re-initialising DB")
        rdb.init_db()
        sleep(5)
        logger.debug(">>>>>>>>>>>> fetching new session")
        new_db = rdb.get_session()

        return new_db        
    else:
        logger.error(">>>>>>>>>>>> DB rebuild skipped, force flag not specified")

        return db



def run_sync(db: Session = Depends(rdb.get_db), sync_type: SyncType = SyncType.update, force=False):

    try:
        logger.info(f">>>>>>>>>>>> sync event triggered, type {sync_type}")

        #check type
        if sync_type not in [ SyncType.update, SyncType.full, SyncType.rebuild ]:
            raise ValueError(f"Sync type {sync_type} not recognised, aborting")

        #check for other active syncs
        active_sync_events: list = access.sync.get_all_ongoing_syncs(db)

        if len(active_sync_events) > 0:
            raise ValueError(f"{len(active_sync_events)} ongoing sync events found, cancelling new sync event")            

        #get last completed sync and its timedelta
        last = access.sync.get_last_sync(db, match_status=SyncStatus.complete, accept_minor = (sync_type == SyncType.update), )

        delta: datetime.timedelta = access.sync.get_sync_delta(last)

        if last is None:
            logger.warn(f">>>>>>>>>>>> WARNING: no recent sync found, performing full sync")
            sync_type = SyncType.full

        #calc acceptable timedelta
        if sync_type in [ SyncType.full, SyncType.rebuild ]:
            accepted_delta = datetime.timedelta(days=SYNC_WAIT_FULL_DAYS) - datetime.timedelta(hours=SYNC_WAIT_FULL_GRACE)
        elif sync_type == SyncType.update:
            accepted_delta = datetime.timedelta(hours=SYNC_WAIT_MINOR_HOURS) - datetime.timedelta(hours=SYNC_WAIT_MINOR_GRACE)
        else:
            raise ValueError(f"Sync type {sync_type} not recognised, aborting")

        #perform the sync
        if force or (delta >= accepted_delta):
            logger.info(f">>>>>>>>>>>> Begin sync, type {sync_type}")

            if sync_type == SyncType.rebuild:
                logger.warn(">>>>>>>>>>>> DROPPING AND REBUILDING DB DURING SYNC")
                db = remake_db(db, force=True)

            sync_start_schema = schemas.sync_schema.SyncCreateSchema(sync_type=sync_type)
            current_event = crud.sync.create(db, sync_start_schema)

            try:
                master.rims_sync_batch_lists(db)

                master.rims_sync_individual(db, skip_existing = (sync_type == SyncType.update))

                master.calc_states(db)

                sync_complete_schema = schemas.sync_schema.SyncCompleteSchema(id=current_event.id, sync_type=current_event.sync_type)
                current_event = crud.sync.update(db, current_event, sync_complete_schema)
                logger.info(f">>>>>>>>>>>> Completed sync, type {sync_type}")
            
            except:
                logger.error(f"!!!!! ERROR: Sync failed, type: {sync_type}")
                sync_complete_schema = schemas.sync_schema.SyncCompleteSchema(id=current_event.id, sync_type=current_event.sync_type, status=SyncStatus.failed)
                current_event = crud.sync.update(db, current_event, sync_complete_schema)

            finally:
                if current_event.status == SyncStatus.in_progress:
                    logger.error(f"!!!!! ERROR: sync not completed, type: {sync_type}, assigning failed")
                    sync_complete_schema = schemas.sync_schema.SyncCompleteSchema(id=current_event.id, sync_type=current_event.sync_type, status=SyncStatus.failed)
                    crud.sync.update(db, current_event, sync_complete_schema)
                else:
                    pass

        else:
            logger.warn(">>>>>>>>>>>> sync event skipped, time difference less than sync frequency")

    except Exception as e:
        logger.error(f"!!!!! ERROR: Sync trigger unsuccessful, type: {sync_type}")        
        logger.error(f"exception content: {str(e)}")
