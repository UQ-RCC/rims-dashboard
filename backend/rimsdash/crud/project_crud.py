from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from backend.rimsdash.crud.base_crud import CRUDBase
from backend.rimsdash.models.project_models import ProjectModel
from backend.rimsdash.schemas.project_schema import ProjectCreateSchema, ProjectUpdateSchema

class CRUDProject(CRUDBase[ProjectModel, ProjectCreateSchema, ProjectUpdateSchema]):
    ...

project = CRUDProject(ProjectModel)