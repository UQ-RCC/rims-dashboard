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


@router.get("/allprojectswithstates", response_model=list[schemas.project_schema.ProjectOutRefsMinSchema])
async def api_getallprojectswithstates(db: Session = Depends(rdb.get_db)): 

    result = []

    __projects = crud.project.get_all(db)

    for project in __projects:
        result.append(schemas.project_schema.ProjectOutRefsMinSchema.validate(project))

    return result


@router.get("/projectdetailwithusers", response_model=schemas.project_schema.ProjectOutRefsSchema)
async def api_projectdetailwithusers(project_id: int, db: Session = Depends(rdb.get_db)): 

    __project = crud.project.get(db, project_id)

    result = schemas.project_schema.ProjectOutRefsSchema.validate(__project)

    return result