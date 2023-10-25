import logging
import rimsdash.config as config
import datetime, pytz
from fastapi import APIRouter, Depends, status
from fastapi_utils.tasks import repeat_every

import rimsdash.db as rdb
import rimsdash.dbgather as dbgather

router = APIRouter()
logger = logging.getLogger('rimsdash')

#from pitschi.db.database import SessionLocal
from fastapi_utils.session import FastAPISessionMaker

sessionmaker = rdb.get_db()

@router.on_event("startup")
@repeat_every(seconds=15, wait_first=False, logger=logger, max_repetitions=1)
def init_admin_user() -> None:
    with sessionmaker.context_session() as db:
        logger.debug(">>>>>>>>>>>> init >>>>>>>>>>>>>>>>>>>>>>>>>>")
        rdb.crud.create_admin_if_not_exist(db)

# every 2 days or so
# sync systems
# sync projects
@router.on_event("startup")
@repeat_every(seconds=60 * 60 * 24 * int(config.get('ppms', 'project_sync_day')), wait_first=False, logger=logger)
def sync_ppms_weekly() -> None:
    logger.debug(">>>>>>>>>>>> Start syncing PPMS projects")
    # first get systems
    # db = SessionLocal()
    with sessionmaker.context_session() as db:
        dbgather.sync_ppms_projects(db, logger)



