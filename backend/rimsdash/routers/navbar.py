import logging
import sys

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
#import rimsdash.db as rdb
#from sqlalchemy.orm import Session

import rimsdash.db as rdb
import rimsdash.crud as crud
import rimsdash.schemas as schemas

router = APIRouter()
logger = logging.getLogger('rimsdash')

@router.get("/userfromemail", response_model=schemas.user_schema.UserTerminalSchema)
async def api_userbyemail(email: str, db: Session = Depends(rdb.get_db)) -> dict:

    __user = crud.user.get_by_email(db, email=email) 

    result = schemas.user_schema.UserTerminalSchema.validate(__user)

    return result.json()

@router.get("/checkadminbyemail")
async def api_adminstatusbyemail(email: str, db: Session = Depends(rdb.get_db)) -> dict:

    __user = crud.user.get_by_email(db, email=email) 

    result = schemas.user_schema.UserReturnAdminSchema.validate(__user)

    return result.json()