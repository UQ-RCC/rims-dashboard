from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi_utils.session import FastAPISessionMaker

import rimsdash.config as config
import rimsdash.db as rdb
import rimsdash.rims as rims
import rimsdash.schemas as schemas
import rimsdash.crud as crud

SQLALCHEMY_DATABASE_URL = (f"{config.get('database', 'type')}://"
                           f"{config.get('database', 'db_username')}:"
                           f"{config.get('database', 'db_password')}@"
                           f"{config.get('database', 'host')}:"
                           f"{config.get('database', 'port')}/"
                           f"{config.get('database', 'db_name')}")

sessionmaker = FastAPISessionMaker(SQLALCHEMY_DATABASE_URL)

def update_systems(db: Session = Depends(rdb.get_db)):
    #get_db() if using fastapi sessionmaker - ?

    systems = rims.get_system_list()

    for system in systems:

        _row = crud.system.get(db, system['id'])

        if _row is None:
            print(f"creating {system['id']}")
            system_in = schemas.SystemCreateSchema(
                id=system['id'],
                type=system['type'],
                name=system['name'],
            )

            crud.system.create(db, system_in)
        else:
            print(f"updating {system['id']}")            
            system_in = schemas.SystemUpdateSchema(
                id=system['id'],
                type=system['type'],
                name=system['name'],
            )

            crud.system.update(db, _row, system_in)


def update_users(db: Session = Depends(rdb.get_db)):
    users = rims.get_userlist()

    for user in users:
        user_in = schemas.UserCreateSchema(
            id=user['id'], \
            name=user['name'], \
            type=user['type'] \
        )
        crud.user.create(db, user_in)
        

def update_projects(db: Session = Depends(rdb.get_db)):
    projects = rims.get_projects()

    for project in projects:
        project_in = schemas.UserCreateSchema(
            id=project['id'], \
            name=project['name'], \
            type=project['type'] \
        )
        crud.user.create(db, project_in)

def run_sync(db: Session = Depends(rdb.get_db)):
    print("starting update")

    update_systems(db)

def initialise():
    print("initialising")

    db = rdb.get_db()    

    rdb.initialise_db(db)

    run_sync(db)        
