from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from rimsdash.crud.base_crud import CRUDBase
from rimsdash.models.projectaccount_models import ProjectAccountModel
from rimsdash.schemas.projectaccount_schema import ProjectAccountReceiveSchema, ProjectAccountUpdateSchema

class CRUDProjectAccount(CRUDBase[ProjectAccountModel, ProjectAccountReceiveSchema, ProjectAccountUpdateSchema]):
    ...

    def get_by_account(self, db: Session, bcode: str):
        return db.query(ProjectAccountModel).filter(ProjectAccountModel.bcode == bcode).all()

    def get_by_project(self, db: Session, project_id: int):
        return db.query(ProjectAccountModel).filter(ProjectAccountModel.project_id == project_id).all()

projectaccount = CRUDProjectAccount(ProjectAccountModel)