from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session
from sqlalchemy import func

from rimsdash.crud.base_crud import CRUDBase
from rimsdash.models.projectusers_models import ProjectUsersModel
from rimsdash.models.project_models import ProjectModel
from rimsdash.schemas.projectusers_schema import ProjectUsersCreateSchema, ProjectUsersUpdateSchema


class CRUDProjectUsers(CRUDBase[ProjectUsersModel, ProjectUsersCreateSchema, ProjectUsersUpdateSchema]):
    ...

    def create(self, db: Session, obj_in: ProjectUsersCreateSchema):

        #create a database object using model and the schema
        db_obj = self.model(
            username = obj_in.username,
            project_id = obj_in.project_id,
            status = obj_in.status
        )

        #add that object and update
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

    def get_by_username(self, db: Session, *, substring: str) -> Optional[list[ProjectUsersModel]]:
        return db.query(ProjectUsersModel).filter(func.lower(ProjectUsersModel.username).contains(substring.lower())).all()

    def get_projects_by_username(self, db: Session, *, username: str) -> Optional[list[ProjectModel]]:
        projects = db.query(ProjectModel).join(ProjectUsersModel).\
            filter(ProjectUsersModel.username == username).all()

        return projects
    
projectuser = CRUDProjectUsers(ProjectUsersModel)