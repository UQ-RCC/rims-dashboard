from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import func

from rimsdash.models import AdminRight
from rimsdash.crud.base_crud import CRUDBase
from rimsdash.models.user_models import UserModel
from rimsdash.schemas.user_schema import UserCreateSchema, UserUpdateSchema

class CRUDUser(CRUDBase[UserModel, UserCreateSchema, UserUpdateSchema]):

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 5000
    ) -> list[UserModel]:
        """
        overwrite the get_multi function to order by username
        """
        return (
            db.query(self.model).order_by(self.model.username).offset(skip).limit(limit).all()
        )

    def get_all(self, db: Session) -> Optional[list[UserModel]]:
        return db.query(UserModel).all()
    
    def get_admins(self, db: Session, *, admin_status: AdminRight = AdminRight.admin) -> Optional[list[UserModel]]:
        return db.query(UserModel).filter(UserModel.admin == admin_status).all()

    def get_by_email(self, db: Session, *, email: str) -> Optional[UserModel]:
        return db.query(UserModel).filter(UserModel.email == email).first()

    def get_by_userid(self, db: Session, *, userid: int) -> Optional[UserModel]:
        return db.query(UserModel).filter(UserModel.userid == userid).one()    

    def get_by_username_substring(self, db: Session, *, substring: str) -> Optional[list[UserModel]]:
        return db.query(UserModel).filter(func.lower(UserModel.username).contains(substring.lower())).all()

    def get_by_name(self, db: Session, *, substring: str) -> Optional[list[UserModel]]:
        return db.query(UserModel).filter(func.lower(UserModel.name).contains(substring.lower())).all()

user = CRUDUser(UserModel)
