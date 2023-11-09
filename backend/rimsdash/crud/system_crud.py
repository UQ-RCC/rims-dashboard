from typing import Optional

from sqlalchemy.orm import Session

from rimsdash.crud.base_crud import CRUDBase
from rimsdash.models.system_models import SystemModel
from rimsdash.schemas.system_schema import SystemCreateSchema, SystemUpdateSchema

class CRUDSystem(CRUDBase[SystemModel, SystemCreateSchema, SystemUpdateSchema]):
    ...

    def sub_search_type(self, db: Session, *, substring: str) -> Optional[list[SystemModel]]:
        return db.query(SystemModel).filter(SystemModel.system_type.contains(substring)).all()

    def sub_search_name(self, db: Session, *, substring: str) -> Optional[SystemModel]:
        return db.query(SystemModel).filter(SystemModel.name.contains(substring)).all()

system = CRUDSystem(SystemModel)