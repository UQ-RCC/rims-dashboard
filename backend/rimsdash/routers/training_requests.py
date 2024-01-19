import logging
import sys

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
#import rimsdash.db as rdb
#from sqlalchemy.orm import Session

import rimsdash.db as rdb
import rimsdash.crud as crud
import rimsdash.repository as repo
import rimsdash.schemas as schemas
import rimsdash.service.generate as generate

router = APIRouter()
logger = logging.getLogger('rimsdash')


@router.get("/alltrequestswithusers", response_model=list[schemas.trequest_schema.TrainingRequestOutSchema])
async def api_getalltrequestswithstates(db: Session = Depends(rdb.get_db)): 

    trequests = crud.trequest.get_all(db)

    result = []

    for trequest in trequests:
        result.append(schemas.trequest_schema.TrainingRequestOutSchema.from_orm(trequest))

    return result

@router.get("/trequestdetail", response_model=schemas.trequest_schema.TrainingRequestOutWithUserStateSchema)
async def api_trequestdetail(trequest_id: int, db: Session = Depends(rdb.get_db)): 

    trequest = crud.trequest.get(db, trequest_id)

    result = schemas.trequest_schema.TrainingRequestOutWithUserStateSchema.from_orm(trequest)

    return result

#schemas.trequest_schema.TrainingRequestMinOutWithStateSchema
@router.get("/trequestsfilterbyid", response_model=list[schemas.trequest_schema.TrainingRequestOutSchema])
async def api_trequestsfilterbyid(trequest_id: int, db: Session = Depends(rdb.get_db)): 

    trequest = crud.trequest.get(db, trequest_id)

    result = [schemas.trequest_schema.TrainingRequestOutSchema.from_orm(trequest)]

    return result

@router.get("/trequestsfilterbytype", response_model=list[schemas.trequest_schema.TrainingRequestOutSchema])
async def api_trequestsfilterbytype(search: str, db: Session = Depends(rdb.get_db)): 

    logger.debug(f"received: {search}")

    trequests = crud.trequest.filter_by_type(db, substring=search)

    result = []

    for trequest in trequests:
        result.append(schemas.trequest_schema.TrainingRequestOutSchema.from_orm(trequest))

    logger.debug(f"schema: {result[0].title}")

    return result

@router.get("/trequestsfilterbyuser", response_model=list[schemas.trequest_schema.TrainingRequestOutSchema])
async def api_trequestsfilterbyuser(search: str, db: Session = Depends(rdb.get_db)): 

    trequests = crud.trequest.filter_by_user_anyname(db, substring=search)

    result = []

    for trequest in trequests:
        result.append(schemas.trequest_schema.TrainingRequestOutSchema.from_orm(trequest))

    return result



"""
UNUSED
"""
@router.get("/trequestsfilterbynew", response_model=list[schemas.trequest_schema.TrainingRequestOutSchema])
async def api_trequestsfilterbynew(search: str, db: Session = Depends(rdb.get_db)): 

    __trequests = repo.trequest.filter_by_title(db, substring=search)

    result = []

    for trequest in __trequests:
        result.append(schemas.trequest_schema.TrainingRequestOutSchema.from_orm(trequest))

    return result