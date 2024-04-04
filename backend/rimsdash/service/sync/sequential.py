
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
        try:
           admin_dict = rims.get_admin_status(user_row.username)
        except: 
            log_sync_error("rims admin status", user_row.username)

        persist.admin_user(user_row, admin_dict, db, skip_existing = skip_existing)