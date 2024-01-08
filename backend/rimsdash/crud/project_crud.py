from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session
from sqlalchemy import func

from rimsdash.crud.base_crud import CRUDBase
from rimsdash.models.project_models import ProjectModel
from rimsdash.schemas.project_schema import ProjectCreateSchema, ProjectUpdateSchema

class CRUDProject(CRUDBase[ProjectModel, ProjectCreateSchema, ProjectUpdateSchema]):
    ...

    def get_all(self, db: Session) -> List[ProjectModel]:
        return db.query(ProjectModel).all()

    def get_by_title(self, db: Session, *, substring: str) -> Optional[list[ProjectModel]]:
        return db.query(ProjectModel).filter(func.lower(ProjectModel.title).contains(substring.lower())).all()

    def get_by_group(self, db: Session, *, substring: str) -> Optional[list[ProjectModel]]:
        return db.query(ProjectModel).filter(func.lower(ProjectModel.group).contains(substring.lower())).all()


project = CRUDProject(ProjectModel)