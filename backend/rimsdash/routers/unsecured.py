import logging

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

import rimsdash.db as rdb
import rimsdash.service.access as access

router = APIRouter()
logger = logging.getLogger('rimsdash')

"""
IMPORTANT: these endpoints are UNSECURED

Use for simple ready check only

"""

@router.get("/ready")
async def api_ready(db: Session = Depends(rdb.get_db)):

    result = { 'ok': True }

    return result


@router.get("/connected")
async def api_connected(db: Session = Depends(rdb.get_db)):

    db_has_cursor: bool = access.sync.has_cursor(db)

    result = { 'connected': db_has_cursor }

    return result


@router.get("/populated")
async def api_populated(db: Session = Depends(rdb.get_db)):

    db_has_synced: bool = access.sync.has_synced(db)

    result = { 'populated': db_has_synced }

    return result