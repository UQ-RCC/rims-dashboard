from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from rimsdash.crud.base_crud import CRUDBase
from rimsdash.models.project_state_models import ProjectStateModel
from rimsdash.schemas.project_state_schema import ProjectStateCreateSchema, ProjectStateUpdateSchema

class CRUDProjectState(CRUDBase[ProjectStateModel, ProjectStateCreateSchema, ProjectStateUpdateSchema]):
    ...

    def get_all(self, db: Session) -> Optional[ProjectStateModel]:
        return db.query(ProjectStateModel).all()

project_state = CRUDProjectState(ProjectStateModel)