
import logging

from sqlalchemy.orm import Session
from fastapi import Depends

import rimsdash.db as rdb
import rimsdash.crud as crud
import rimsdash.external.rims as rims
import rimsdash.service.sync.persist as persist

from .utils import log_sync_error

logger = logging.getLogger('rimsdash')

def admin_users(db: Session = Depends(rdb.get_db), skip_existing: bool = False):
    """
    Sync admin status in DB to external RIMS DB
    """
    logger.info(f"Syncing admin status")

    for user_row in crud.user.get_all(db):
        persist.admin_user(user_row, db, skip_existing = skip_existing)