from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from backend.rimsdash.crud.base_crud import CRUDBase
from backend.rimsdash.models.user_models import UserModel
from backend.rimsdash.schemas.user_schema import UserCreateSchema, UserUpdateSchema

class CRUDUser(CRUDBase[UserModel, UserCreateSchema, UserUpdateSchema]):

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 5000
    ) -> List[UserModel]:
        """
        overwrite the get_multi function to order by username
        """
        return (
            db.query(self.model).order_by(self.model.username).offset(skip).limit(limit).all()
        )

    def get_by_email(self, db: Session, *, email: str) -> Optional[UserModel]:
        return db.query(UserModel).filter(UserModel.email == email).first()

    def get_by_userid(self, db: Session, *, userid: int) -> Optional[UserModel]:
        return db.query(UserModel).filter(UserModel.userid == userid).first()

user = CRUDUser(UserModel)
