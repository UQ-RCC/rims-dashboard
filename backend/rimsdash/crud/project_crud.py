from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from rimsdash.crud.base_crud import CRUDBase
from rimsdash.models.project_models import ProjectModel
from rimsdash.schemas.project_schema import ProjectCreateSchema, ProjectUpdateSchema

class CRUDProject(CRUDBase[ProjectModel, ProjectCreateSchema, ProjectUpdateSchema]):
    ...

    def get_all(self, db: Session) -> List[ProjectModel]:
        return db.query(ProjectModel).all()

project = CRUDProject(ProjectModel)