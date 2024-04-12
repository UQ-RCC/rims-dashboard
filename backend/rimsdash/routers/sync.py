import logging
import rimsdash.config as config
import datetime
from fastapi import APIRouter, Depends, status
from fastapi_utils.tasks import repeat_every

import rimsdash.db as rdb
import rimsdash.service.sync as sync

router = APIRouter()
logger = logging.getLogger('rimsdash')

# every day, sync database to RIMS
@router.on_event("startup")
@repeat_every(seconds=60 * 60 * 24, wait_first=False, logger=logger)
def sync_daily() -> None:

    if True:        
        logger.info(">>>>>>>>>>>>Initialising DB")
        rdb.init_db()

    with rdb.sessionmaker.context_session() as db:
            sync.control.run_sync(db, force=False)

