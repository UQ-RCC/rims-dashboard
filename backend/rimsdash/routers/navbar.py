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

MESSAGE_DENIED = "access denied"

@router.get("/user")
async def get_user(user: dict = Depends(keycloak.decode)):
    logger.debug("Querying user")
    return user

@router.get("/token")
async def get_token(token: str = Depends(keycloak.oauth2_scheme)):
    logger.debug("Querying token")
    return token


@router.get("/adminfromtoken", response_model=schemas.user_schema.UserAdminOutSchema)
async def api_adminfromtoken(db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)):
    """
    return the admin status corresponding to the keycloak token
    """
    try:
        logger.info(f"Admin request for {keycloak_user.email}")
    except:
        pass

    try:
        has_access = service.security.lookup_user(db, keycloak_user)
    except Exception as e:
        logger.exception("Keycloak data not valid")
        return JSONResponse(status_code=401, content={"message": str(e)})

    if has_access:
        try:
            __user = crud.user.get_by_email(db, email=keycloak_user.get('email')) 

            result = schemas.user_schema.UserAdminOutSchema.from_orm(__user)
        except:
            return JSONResponse(status_code=400, content={"message": str(e)})
        
        finally:
            return result
    else:
        logger.error(f"Access=false passed without exception for keycloak {keycloak_user.get('email')}")
        return JSONResponse(status_code=401, content={"message": MESSAGE_DENIED})

@router.get("/userfromtoken", response_model=schemas.user_schema.UserSelfOutSchema)
async def api_userfromtoken(db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)):
    """
    return the userdata corresponding to the keycloak token
    """
    try:
        logger.info(f"Access request for {keycloak_user.get('email')}")
    except:
        pass

    try:
        has_access = service.security.lookup_user(db, keycloak_user)
    except Exception as e:
        logger.exception("Keycloak data not valid")
        return JSONResponse(status_code=401, content={"message": str(e)})

    try:
        __user = crud.user.get_by_email(db, email=keycloak_user.get('email')) 

        result = schemas.user_schema.UserSelfOutSchema.from_orm(__user)
    except:
        return JSONResponse(status_code=400, content={"message": str(e)})
    
    finally:
        return result

@router.get("/userfromemail", response_model=schemas.user_schema.UserOutSchema)
async def api_userbyemail(email: str, db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)):

    try:
        has_access = service.security.lookup_admin_rights(db, keycloak_user)
    except Exception as e:
        logger.exception("Access denied by keycloak")
        return JSONResponse(status_code=401, content={"message": str(e)})

    if has_access:
        __user = crud.user.get_by_email(db, email=email) 

        result = schemas.user_schema.UserOutSchema.from_orm(__user)

        return result
    else:
        logger.error(f"Access=false passed without exception for keycloak {keycloak_user.get('email')}")
        return JSONResponse(status_code=401, content={"message": MESSAGE_DENIED})

@router.get("/checkadminbyemail", response_model=schemas.user_schema.UserReturnAdminSchema)
async def api_adminstatusbyemail(email: str, db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)):

    try:
        has_access = service.security.lookup_admin_rights(db, keycloak_user)
    except Exception as e:
        logger.exception("Access denied by keycloak")
        return JSONResponse(status_code=401, content={"message": str(e)})

    if has_access:
        __user = crud.user.get_by_email(db, email=email) 

        result = schemas.user_schema.UserReturnAdminSchema.from_orm(__user)

        return result
    else:
        logger.error(f"Access=false passed without exception for keycloak {keycloak_user.get('email')}")
        return JSONResponse(status_code=401, content={"message": MESSAGE_DENIED})

@router.get("/checkwhitelistbyemail", response_model=schemas.WhitelistSchema)
async def api_checkwhitelistbyemail(email: str, db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)):
    """
    check if user is in config whitelist

    accepts if email found, or whitelist is empty

    DEPRECATED
    """

    try:
        has_access = service.security.lookup_admin_rights(db, keycloak_user)
    except Exception as e:
        logger.exception("Access denied by keycloak")
        return JSONResponse(status_code=401, content={"message": str(e)})

    if has_access:
        __user = crud.user.get_by_email(db, email=email) 

        whitelist=config.get_csv_list("manual","whitelist")

        status=(__user.email in whitelist or whitelist=='' or whitelist is None)

        result = schemas.WhitelistSchema(email=__user.email, whitelist=status)
        
        logger.info(f"whitelist return {email}, {result.whitelist}")

        return result
    else:
        logger.error(f"Access=false passed without exception for keycloak {keycloak_user.get('email')}")
        return JSONResponse(status_code=401, content={"message": MESSAGE_DENIED})


@router.get("/getadminlist")
async def api_adminslist(db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)) -> str:
    """
    return list of admin users

    FUTURE: maybe move this to an internal function
    """

    try:
        has_access = service.security.lookup_admin_rights(db, keycloak_user)
    except Exception as e:
        logger.exception("Access denied by keycloak")
        return JSONResponse(status_code=401, content={"message": str(e)})

    if has_access:
        admins = crud.user.get_admins(db, admin_status=False)

        result = []

        for admin in admins:
            result.append(schemas.user_schema.UserOutSchema.from_orm(admin).json())

        return result
    else:
        logger.error(f"Access=false passed without exception for keycloak {keycloak_user.get('email')}")
        return JSONResponse(status_code=401, content={"message": MESSAGE_DENIED})
