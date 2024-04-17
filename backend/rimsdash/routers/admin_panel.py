
import logging
import sys

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

import rimsdash.db as rdb
import rimsdash.crud as crud
import rimsdash.repository as repo
import rimsdash.schemas as schemas
import rimsdash.service.access as access
import rimsdash.utils.keycloak as keycloak
import rimsdash.service as service

from rimsdash.models import SyncType


router = APIRouter()
logger = logging.getLogger('rimsdash')

MESSAGE_DENIED = "access denied"
MESSAGE_SERVER_ERROR = "Internal Server Error: The function did not complete as expected."

@router.get("/getlastsync", response_model=list[schemas.sync_schema.SyncOutSchema])
async def api_getlastsync(db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)): 
    try:
        has_access = service.security.lookup_admin_rights(db, keycloak_user)
    except Exception as e:
        logger.exception("Access denied by keycloak")
        return JSONResponse(status_code=401, content={"message": str(e)})

    if has_access:
        row = access.sync.db_last_sync(db, accept_minor = True)

        result = [schemas.sync_schema.SyncOutSchema.from_orm(row)]

        return result
    else:
        logger.error(f"Access=false passed without exception for keycloak {keycloak_user.get('email')}")
        return JSONResponse(status_code=401, content={"message": MESSAGE_DENIED})


@router.get("/getlastfullsync", response_model=list[schemas.sync_schema.SyncOutSchema])
async def api_getlastfullsync(db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)): 
    try:
        has_access = service.security.lookup_admin_rights(db, keycloak_user)
    except Exception as e:
        logger.exception("Access denied by keycloak")
        return JSONResponse(status_code=401, content={"message": str(e)})

    if has_access:
        row = access.sync.db_last_sync(db, accept_minor = False)

        result = [schemas.sync_schema.SyncOutSchema.from_orm(row)]

        return result
    else:
        logger.error(f"Access=false passed without exception for keycloak {keycloak_user.get('email')}")
        return JSONResponse(status_code=401, content={"message": MESSAGE_DENIED})    


@router.get("/allsyncs", response_model=list[schemas.sync_schema.SyncOutSchema])
async def api_allsyncs(db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)): 
    try:
        has_access = service.security.lookup_admin_rights(db, keycloak_user)
    except Exception as e:
        logger.exception("Access denied by keycloak")
        return JSONResponse(status_code=401, content={"message": str(e)})

    if has_access:
        __syncs = access.sync.get_all_recent_syncs(db)

        result = []

        for sync in __syncs:
            result.append(schemas.sync_schema.SyncOutSchema.from_orm(sync))

        return result
    else:
        logger.error(f"Access=false passed without exception for keycloak {keycloak_user.get('email')}")
        return JSONResponse(status_code=401, content={"message": MESSAGE_DENIED})    



@router.post("/manualsyncupdate")
async def api_manualsyncupdate(db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)): 
    try:
        has_access = service.security.lookup_realm_rights(db, keycloak_user)    #requires realm, not just admin
    except Exception as e:
        logger.exception("Access denied by keycloak")
        return JSONResponse(status_code=401, content={"message": str(e)})

    if has_access:
        try:
            service.sync.control.run_sync(db, sync_type = SyncType.update, force=True)

            return JSONResponse(status_code=204)
           
        except:
            return JSONResponse(status_code=500, content={"message": MESSAGE_SERVER_ERROR})

    else:
        logger.error(f"Access=false passed without exception for keycloak {keycloak_user.get('email')}")
        return JSONResponse(status_code=401, content={"message": MESSAGE_DENIED})    


@router.post("/manualsyncfull")
async def api_manualsyncfull(db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)): 
    try:
        has_access = service.security.lookup_realm_rights(db, keycloak_user)    #requires realm, not just admin
    except Exception as e:
        logger.exception("Access denied by keycloak")
        return JSONResponse(status_code=401, content={"message": str(e)})

    if has_access:
        try:
            service.sync.control.run_sync(db, sync_type = SyncType.full, force=True)

            return JSONResponse(status_code=204)
        
        except:
            return JSONResponse(status_code=500, content={"message": MESSAGE_SERVER_ERROR})

    else:
        logger.error(f"Access=false passed without exception for keycloak {keycloak_user.get('email')}")
        return JSONResponse(status_code=401, content={"message": MESSAGE_DENIED})  


@router.post("/manualsyncfullrebuild")
async def api_manualsyncfullrebuild(db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)): 
    try:
        has_access = service.security.lookup_realm_rights(db, keycloak_user)    #requires realm, not just admin
    except Exception as e:
        logger.exception("Access denied by keycloak")
        return JSONResponse(status_code=401, content={"message": str(e)})

    if has_access:
        try:
            service.sync.control.run_sync(db, sync_type = SyncType.full, force=True, rebuild=True)

            return JSONResponse(status_code=204)
        
        except:
            return JSONResponse(status_code=500, content={"message": MESSAGE_SERVER_ERROR})
    else:
        logger.error(f"Access=false passed without exception for keycloak {keycloak_user.get('email')}")
        return JSONResponse(status_code=401, content={"message": MESSAGE_DENIED})  