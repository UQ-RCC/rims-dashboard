import logging
import sys

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

import rimsdash.db as rdb
import rimsdash.crud as crud
import rimsdash.repository as repo
import rimsdash.schemas as schemas
import rimsdash.service.generate as generate
import rimsdash.utils.keycloak as keycloak
import rimsdash.service as service

router = APIRouter()
logger = logging.getLogger('rimsdash')

FALLBACK_ERROR = JSONResponse(status_code=400, content={"message": "request not completed"})

@router.get("/alltrequests", response_model=list[schemas.trequest_schema.TrainingRequestOutSchema])
async def api_getalltrequests(db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)):
    try:
        has_access = service.processing.lookup_keycloak_user_access(db, keycloak_user)
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

    if has_access:
        trequests = crud.trequest.get_all(db)

        result = []

        for trequest in trequests:
            result.append(schemas.trequest_schema.TrainingRequestOutSchema.from_orm(trequest))

        return result
    else:
        return FALLBACK_ERROR
    
@router.get("/alltrequestswithusers", response_model=list[schemas.trequest_schema.TrainingRequestOutWithUserSchema])
async def api_getalltrequestswithusers(db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)): 
    try:
        has_access = service.processing.lookup_keycloak_user_access(db, keycloak_user)
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

    if has_access:
        trequests = crud.trequest.get_all(db)

        result = []

        for trequest in trequests:
            result.append(schemas.trequest_schema.TrainingRequestOutWithUserSchema.from_orm(trequest))

        return result
    else:
        return FALLBACK_ERROR
    
@router.get("/trequestdetail", response_model=schemas.trequest_schema.TrainingRequestOutWithUserStateSchema)
async def api_trequestdetail(trequest_id: int, db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)): 
    try:
        has_access = service.processing.lookup_keycloak_user_access(db, keycloak_user)
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

    if has_access:
        trequest = crud.trequest.get(db, trequest_id)

        result = schemas.trequest_schema.TrainingRequestOutWithUserStateSchema.from_orm(trequest)

        return result
    else:
        return FALLBACK_ERROR
    
#schemas.trequest_schema.TrainingRequestMinOutWithStateSchema
@router.get("/trequestsfilterbyid", response_model=list[schemas.trequest_schema.TrainingRequestOutWithUserSchema])
async def api_trequestsfilterbyid(trequest_id: int, db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)): 
    try:
        has_access = service.processing.lookup_keycloak_user_access(db, keycloak_user)
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

    if has_access:
        trequest = crud.trequest.get(db, trequest_id)

        result = [schemas.trequest_schema.TrainingRequestOutWithUserSchema.from_orm(trequest)]

        return result
    else:
        return FALLBACK_ERROR
    
@router.get("/trequestsfilterbytype", response_model=list[schemas.trequest_schema.TrainingRequestOutWithUserSchema])
async def api_trequestsfilterbytype(search: str, db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)): 
    try:
        has_access = service.processing.lookup_keycloak_user_access(db, keycloak_user)
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

    if has_access:
        logger.debug(f"received: {search}")

        trequests = crud.trequest.filter_by_type(db, substring=search)

        result = []

        for trequest in trequests:
            result.append(schemas.trequest_schema.TrainingRequestOutWithUserSchema.from_orm(trequest))

        return result
    else:
        return FALLBACK_ERROR
    
@router.get("/trequestsfilterbyuser", response_model=list[schemas.trequest_schema.TrainingRequestOutWithUserSchema])
async def api_trequestsfilterbyuser(substring: str, db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)): 
    try:
        has_access = service.processing.lookup_keycloak_user_access(db, keycloak_user)
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

    if has_access:
        trequests = crud.trequest.filter_by_user_anyname(db, substring=substring)

        result = []

        for trequest in trequests:
            result.append(schemas.trequest_schema.TrainingRequestOutWithUserSchema.from_orm(trequest))

        return result
    else:
        return FALLBACK_ERROR
    


"""
UNUSED
"""
@router.get("/trequestsfilterbynew", response_model=list[schemas.trequest_schema.TrainingRequestOutWithUserSchema])
async def api_trequestsfilterbynew(search: str, db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)): 
    try:
        has_access = service.processing.lookup_keycloak_user_access(db, keycloak_user)
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

    if has_access:
        __trequests = repo.trequest.filter_by_title(db, substring=search)

        result = []

        for trequest in __trequests:
            result.append(schemas.trequest_schema.TrainingRequestOutWithUserSchema.from_orm(trequest))

        return result
    else:
        return FALLBACK_ERROR    