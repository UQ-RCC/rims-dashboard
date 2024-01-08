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


@router.get("/allprojectswithstates", response_model=list[schemas.project_schema.ProjectMinOutWithStateSchema])
async def api_getallprojectswithstates(db: Session = Depends(rdb.get_db)): 

    project_generator = generate.generate_projects(db)

    result = []

    for project in project_generator:
        result.append(schemas.project_schema.ProjectMinOutWithStateSchema.from_orm(project))

    return result

@router.get("/allprojectswithfullstates", response_model=list[schemas.project_schema.ProjectOutRefsSchema])
async def api_getallprojectswithfullstates(db: Session = Depends(rdb.get_db)): 

    project_generator = generate.generate_projects(db)

    result = []

    for project in project_generator:
        result.append(schemas.project_schema.ProjectOutRefsSchema.from_orm(project))

    return result


@router.get("/projectdetailwithusers", response_model=schemas.project_schema.ProjectOutRefsSchema)
async def api_projectdetailwithusers(project_id: int, db: Session = Depends(rdb.get_db)): 

    __project = crud.project.get(db, project_id)

    result = schemas.project_schema.ProjectOutRefsSchema.from_orm(__project)

    return result


@router.get("/projectgetbyid", response_model=schemas.project_schema.ProjectMinOutWithStateSchema)
async def api_projectgetbyid(project_id: int, db: Session = Depends(rdb.get_db)): 

    __project = repo.project.get_by_id(db, project_id=project_id)

    result = schemas.project_schema.ProjectMinOutWithStateSchema.from_orm(__project)

    return result


@router.get("/projectsgetbytitle", response_model=schemas.project_schema.ProjectMinOutWithStateSchema)
async def api_projectsgetbytitle(substring: str, db: Session = Depends(rdb.get_db)): 

    __projects = repo.project.filter_by_title(db, substring=substring)

    result = []

    for project in __projects:
        result.append(schemas.project_schema.ProjectMinOutWithStateSchema.from_orm(project))

    return result

@router.get("/projectsgetbygroup", response_model=schemas.project_schema.ProjectMinOutWithStateSchema)
async def api_projectsgetbygroup(substring: str, db: Session = Depends(rdb.get_db)): 

    __projects = repo.project.filter_by_group(db, substring=substring)

    result = []

    for project in __projects:
        result.append(schemas.project_schema.ProjectMinOutWithStateSchema.from_orm(project))

    return result

@router.get("/projectsgetbyuser", response_model=schemas.project_schema.ProjectMinOutWithStateSchema)
async def api_projectsgetbyuser(substring: str, db: Session = Depends(rdb.get_db)): 

    __projects = repo.project.filter_projects_by_user_allnames(db, substring=substring)

    result = []

    for project in __projects:
        result.append(schemas.project_schema.ProjectMinOutWithStateSchema.from_orm(project))

    return result