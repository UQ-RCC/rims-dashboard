import logging
import sys

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

import rimsdash.config as config
import rimsdash.db as rdb
import rimsdash.crud as crud
import rimsdash.schemas as schemas
import rimsdash.utils.keycloak as keycloak
import rimsdash.service as service

router = APIRouter()
logger = logging.getLogger('rimsdash')

FALLBACK_ERROR = JSONResponse(status_code=400, content={"message": "request not completed"})

@router.get("/ready")
async def api_ready(db: Session = Depends(rdb.get_db), user: dict = Depends(keycloak.decode)):

    result = { 'ok': True }

    return result

@router.get("/user")
async def get_user(user: dict = Depends(keycloak.decode)):
    logger.debug("Querying user")
    return user

@router.get("/token")
async def get_token(token: str = Depends(keycloak.oauth2_scheme)):
    logger.debug("Querying token")
    return token

@router.get("/userfromemail", response_model=schemas.user_schema.UserOutSchema)
async def api_userbyemail(email: str, db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)):

    try:
        has_access = service.processing.lookup_keycloak_user_access(db, keycloak_user)
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

    if has_access:
        __user = crud.user.get_by_email(db, email=email) 

        result = schemas.user_schema.UserOutSchema.from_orm(__user)

        return result
    else:
        return FALLBACK_ERROR

@router.get("/checkadminbyemail", response_model=schemas.user_schema.UserReturnAdminSchema)
async def api_adminstatusbyemail(email: str, db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)):

    try:
        has_access = service.processing.lookup_keycloak_user_access(db, keycloak_user)
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

    if has_access:
        __user = crud.user.get_by_email(db, email=email) 

        result = schemas.user_schema.UserReturnAdminSchema.from_orm(__user)

        return result
    else:
        return FALLBACK_ERROR

@router.get("/checkwhitelistbyemail", response_model=schemas.WhitelistSchema)
async def api_checkwhitelistbyemail(email: str, db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)):
    """
    check if user is in config whitelist

    accepts if email found, or whitelist is empty

    DEPRECATED
    """

    try:
        has_access = service.processing.lookup_keycloak_user_access(db, keycloak_user)
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

    if has_access:
        __user = crud.user.get_by_email(db, email=email) 

        whitelist=config.get_csv_list("manual","whitelist")

        status=(__user.email in whitelist or whitelist=='' or whitelist is None)

        result = schemas.WhitelistSchema(email=__user.email, whitelist=status)
        
        logger.info(f"whitelist return {email}, {result.whitelist}")

        return result
    else:
        return FALLBACK_ERROR


@router.get("/getadminlist")
async def api_adminslist(db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)) -> str:
    """
    return list of admin users

    FUTURE: maybe move this to an internal function
    """

    try:
        has_access = service.processing.lookup_keycloak_user_access(db, keycloak_user)
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

    if has_access:
        admins = crud.user.get_admins(db, admin_status=False)

        result = []

        for admin in admins:
            result.append(schemas.user_schema.UserOutSchema.from_orm(admin).json())

        return result
    else:
        return FALLBACK_ERROR
