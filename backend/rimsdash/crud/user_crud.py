from typing import Optional

from sqlalchemy.orm import Session

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

    def get_by_email(self, db: Session, *, email: str) -> Optional[UserModel]:
        return db.query(UserModel).filter(UserModel.email == email).first()

    def get_by_userid(self, db: Session, *, userid: int) -> Optional[UserModel]:
        return db.query(UserModel).filter(UserModel.userid == userid).one()

    def get_all(self, db: Session) -> Optional[list[UserModel]]:
        return db.query(UserModel).all()
    
    def get_admins(self, db: Session, *, admin_status: bool = True) -> Optional[list[UserModel]]:
        return db.query(UserModel).filter(UserModel.admin == admin_status).all()


user = CRUDUser(UserModel)
