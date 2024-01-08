import logging
import rimsdash.config as config
import datetime
from fastapi import APIRouter, Depends, status
from fastapi_utils.tasks import repeat_every

import rimsdash.db as rdb
import rimsdash.service.processing as processing

router = APIRouter()
logger = logging.getLogger('rimsdash')

# every day, sync database to RIMS
@router.on_event("startup")
@repeat_every(seconds=60 * 60 * 24, wait_first=False, logger=logger)
def sync_daily() -> None:

    #if not rdb.exists():
    if True:        
        logger.info(">>>>>>>>>>>>Initialising DB")
        rdb.init_db()
    else:
        logger.info(">>>>>>>>>>>>DB already initialised")

    logger.info(">>>>>>>>>>>>Sync event triggered")
    with rdb.sessionmaker.context_session() as db:
            processing.primary_sync(db, force=False)



