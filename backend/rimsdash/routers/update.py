import rimsdash.config as config
import rimsdash.db as rdb
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
import rimsdash.rims as rims
from fastapi_utils.session import FastAPISessionMaker

SQLALCHEMY_DATABASE_URL = (f"{config.get('database', 'type')}://"
                           f"{config.get('database', 'db_username')}:"
                           f"{config.get('database', 'db_password')}@"
                           f"{config.get('database', 'host')}:"
                           f"{config.get('database', 'port')}/"
                           f"{config.get('database', 'db_name')}")

sessionmaker = FastAPISessionMaker(SQLALCHEMY_DATABASE_URL)

print("starting")

def update_systems(db: Session = Depends(rdb.get_db)):

    systems = rims.get_system_list()

    #clear the table (disabled) 
    if False and systems != []:
        rdb.crud.clear_systems(db)

    for system in systems:
        system_schema = rdb.schemas.System( \
                                    id=system['id'], \
                                    name=system['name'], \
                                    type=system['type'] \
                                )
        
        rdb.crud.update_system(db, system_schema)

def update_users(db: Session = Depends(rdb.get_db)):
    users = rims.get_userlist()

    for user in users:
        rdb.crud.create_user(db, rdb.schemas.User( \
                                    id=user['id'], \
                                    name=user['name'], \
                                    type=user['type'] \
                                ))

def update_projects(db: Session = Depends(rdb.get_db)):
    projects = rims.get_system_list()

    for project in projects:
        rdb.crud.create_project(db, rdb.schemas.Project( \
                                    id=project['id'], \
                                    name=project['name'], \
                                    type=project['type'] \
                                ))

def run_sync():
    with sessionmaker.context_session() as db:
        update_systems(db)
