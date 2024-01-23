import logging

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

import rimsdash.db as rdb

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