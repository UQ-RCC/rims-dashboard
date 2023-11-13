from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from rimsdash.crud.base_crud import CRUDBase
from rimsdash.models.system_user_rights_models import SystemUserRightsModel
from rimsdash.schemas.system_user_rights_schema import SystemUserRightsCreateSchema, SystemUserRightsUpdateSchema

class CRUDSystemUserRights(CRUDBase[SystemUserRightsModel, SystemUserRightsCreateSchema, SystemUserRightsUpdateSchema]):
    ...

    def create(self, db: Session, obj_in: SystemUserRightsCreateSchema):

        #create a database object using model and the schema
        db_obj = self.model(
            username = obj_in.username,
            system_id = obj_in.system_id,
            status = obj_in.status
        )

        #add that object and update
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

    def get_by_user(self, db: Session, username: str):
        return db.query(SystemUserRightsModel).filter(SystemUserRightsModel.username == username).all()

    def get_by_system(self, db: Session, system_id: int):
        return db.query(SystemUserRightsModel).filter(SystemUserRightsModel.system_id == system_id).all()

system_user_rights = CRUDSystemUserRights(SystemUserRightsModel)