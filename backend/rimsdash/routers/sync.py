import logging
import rimsdash.config as config
import datetime
from fastapi import APIRouter, Depends, status
from fastapi_utils.tasks import repeat_every

import rimsdash.db as rdb
import rimsdash.collate.processing as processing

router = APIRouter()
logger = logging.getLogger('rimsdash')

# every day, sync database to RIMS
@router.on_event("startup")
@repeat_every(seconds=60 * 60 * 24, wait_first=False, logger=logger)
def sync_daily() -> None:
    logger.info(">>>>>>>>>>>> Begin syncing to RIMS")
    with rdb.sessionmaker.context_session() as db:
        processing.sync_systems(db)
        processing.sync_users(db)
        processing.sync_projects(db)
        processing.sync_user_rights(db)
        processing.sync_project_users(db)
        processing.sync_user_admin(db, skip_existing = True)
        logger.info(">>>>>>>>>>>> Finished syncing to RIMS") 

        logger.info(">>>>>>>>>>>> Begin calculating states")
        processing.process_projects(db)
        processing.process_users(db)
        logger.info(">>>>>>>>>>>> Finished calculating states")        
             



