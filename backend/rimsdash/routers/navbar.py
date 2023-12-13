import logging
import sys

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
#import rimsdash.db as rdb
#from sqlalchemy.orm import Session

import rimsdash.config as config
import rimsdash.db as rdb
import rimsdash.crud as crud
import rimsdash.schemas as schemas

router = APIRouter()
logger = logging.getLogger('rimsdash')


@router.get("/ready")
async def api_ready(db: Session = Depends(rdb.get_db)):

    result = { 'ok': True }

    return result


@router.get("/userfromemail", response_model=schemas.user_schema.UserOutSchema)
async def api_userbyemail(email: str, db: Session = Depends(rdb.get_db)):

    __user = crud.user.get_by_email(db, email=email) 

    result = schemas.user_schema.UserOutSchema.from_orm(__user)

    return result

@router.get("/checkadminbyemail", response_model=schemas.user_schema.UserReturnAdminSchema)
async def api_adminstatusbyemail(email: str, db: Session = Depends(rdb.get_db)):

    __user = crud.user.get_by_email(db, email=email) 

    result = schemas.user_schema.UserReturnAdminSchema.from_orm(__user)

    return result


@router.get("/checkwhitelistbyemail", response_model=schemas.WhitelistSchema)
async def api_checkwhitelistbyemail(email: str, db: Session = Depends(rdb.get_db)):
    """
    check if user is in config whitelist

    accepts if email found, or whitelist is empty
    """
    __user = crud.user.get_by_email(db, email=email) 

    whitelist=config.get("manual","whitelist")
    whitelist=whitelist.replace(' ', '')
    whitelist=whitelist.split(',')

    status=(__user.email in whitelist or whitelist=='' or whitelist is None)

    result = schemas.WhitelistSchema(email=__user.email, whitelist=status)
    
    logger.info(f"whitelist return {email}, {result.whitelist}")

    return result



@router.get("/getadminlist")
async def api_adminslist(db: Session = Depends(rdb.get_db)) -> str:
    """
    return list of admin users

    FUTURE: maybe move this to an internal function
    """

    admins = crud.user.get_admins(db, admin_status=False)

    result = []

    for admin in admins:
        result.append(schemas.user_schema.UserOutSchema.from_orm(admin).json())

    return result

