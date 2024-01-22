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

@router.get("/allprojectswithstates", response_model=list[schemas.project_schema.ProjectMinOutWithStateSchema])
async def api_getallprojectswithstates(db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)): 
    try:
        has_access = service.processing.lookup_keycloak_user_access(db, keycloak_user)
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

    if has_access:
        project_generator = generate.generate_projects(db)

        result = []

        for project in project_generator:
            result.append(schemas.project_schema.ProjectMinOutWithStateSchema.from_orm(project))

        return result
    else:
        return FALLBACK_ERROR
    
@router.get("/allprojectswithfullstates", response_model=list[schemas.project_schema.ProjectOutRefsSchema])
async def api_getallprojectswithfullstates(db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)): 
    try:
        has_access = service.processing.lookup_keycloak_user_access(db, keycloak_user)
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

    if has_access:
        project_generator = generate.generate_projects(db)

        result = []

        for project in project_generator:
            result.append(schemas.project_schema.ProjectOutRefsSchema.from_orm(project))

        return result
    else:
        return FALLBACK_ERROR

@router.get("/projectdetailwithusers", response_model=schemas.project_schema.ProjectOutRefsSchema)
async def api_projectdetailwithusers(project_id: int, db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)): 
    try:
        has_access = service.processing.lookup_keycloak_user_access(db, keycloak_user)
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

    if has_access:
        __project = crud.project.get(db, project_id)

        result = schemas.project_schema.ProjectOutRefsSchema.from_orm(__project)

        return result
    else:
        return FALLBACK_ERROR

#schemas.project_schema.ProjectMinOutWithStateSchema
@router.get("/projectgetbyid", response_model=list[schemas.project_schema.ProjectMinOutWithStateSchema])
async def api_projectgetbyid(project_id: int, db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)): 
    try:
        has_access = service.processing.lookup_keycloak_user_access(db, keycloak_user)
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

    if has_access:
        __project = repo.project.get_by_id(db, project_id=project_id)

        result = [schemas.project_schema.ProjectMinOutWithStateSchema.from_orm(__project)]

        return result
    else:
        return FALLBACK_ERROR

@router.get("/projectsgetbytitle", response_model=list[schemas.project_schema.ProjectMinOutWithStateSchema])
async def api_projectsgetbytitle(search: str, db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)): 
    try:
        has_access = service.processing.lookup_keycloak_user_access(db, keycloak_user)
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

    if has_access:
        __projects = repo.project.filter_by_title(db, substring=search)

        result = []

        for project in __projects:
            result.append(schemas.project_schema.ProjectMinOutWithStateSchema.from_orm(project))

        return result
    else:
        return FALLBACK_ERROR
    
@router.get("/projectsgetbygroup", response_model=list[schemas.project_schema.ProjectMinOutWithStateSchema])
async def api_projectsgetbygroup(search: str, db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)): 
    try:
        has_access = service.processing.lookup_keycloak_user_access(db, keycloak_user)
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

    if has_access:
        logger.debug(f"received: {search}")

        __projects = repo.project.filter_by_group(db, substring=search)

        logger.debug(f"found: {__projects[0].title}")

        result = []

        for project in __projects:
            result.append(schemas.project_schema.ProjectMinOutWithStateSchema.from_orm(project))

        logger.debug(f"schema: {result[0].title}")

        return result
    else:
        return FALLBACK_ERROR

@router.get("/projectsgetbyuser", response_model=list[schemas.project_schema.ProjectMinOutWithStateSchema])
async def api_projectsgetbyuser(search: str, db: Session = Depends(rdb.get_db), keycloak_user: dict = Depends(keycloak.decode)): 
    try:
        has_access = service.processing.lookup_keycloak_user_access(db, keycloak_user)
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

    if has_access:
        __projects = repo.project.filter_projects_by_user_allnames(db, substring=search)

        result = []

        for project in __projects:
            result.append(schemas.project_schema.ProjectMinOutWithStateSchema.from_orm(project))

        return result
    else:
        return FALLBACK_ERROR    