from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from rimsdash.crud.base_crud import CRUDBase
from rimsdash.models.user_state_models import UserStateModel
from rimsdash.schemas.user_state_schema import UserStateCreateSchema, UserStateUpdateSchema

class CRUDUserState(CRUDBase[UserStateModel, UserStateCreateSchema, UserStateUpdateSchema]):
    ...

    def get_all(self, db: Session) -> Optional[UserStateModel]:
        return db.query(UserStateModel).all()

user_state = CRUDUserState(UserStateModel)