from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from rimsdash.crud.base_crud import CRUDBase
from rimsdash.models.projectusers_models import ProjectUsersModel
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

projectuser = CRUDProjectUsers(ProjectUsersModel)