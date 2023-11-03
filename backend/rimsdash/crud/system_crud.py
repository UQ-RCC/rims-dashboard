from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from backend.rimsdash.crud.base_crud import CRUDBase
from backend.rimsdash.models.system_models import SystemModel
from backend.rimsdash.schemas.system_schema import SystemCreateSchema, SystemUpdateSchema

class CRUDSystem(CRUDBase[SystemModel, SystemCreateSchema, SystemUpdateSchema]):
    ...

system = CRUDSystem(SystemModel)