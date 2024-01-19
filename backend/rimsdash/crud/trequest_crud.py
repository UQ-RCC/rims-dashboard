from typing import Optional, List

from sqlalchemy.orm import Session
from sqlalchemy import func

from rimsdash.crud.base_crud import CRUDBase
from rimsdash.models.user_models import UserModel
from rimsdash.models.trequest_models import TrainingRequestModel
from rimsdash.schemas.trequest_schema import TrainingRequestCreateSchema, TrainingRequestUpdateSchema

class CRUDTrainingRequest(CRUDBase[TrainingRequestModel, TrainingRequestCreateSchema, TrainingRequestUpdateSchema]):
    ...

    def get_all(self, db: Session) -> List[TrainingRequestModel]:
        return db.query(TrainingRequestModel).all()

    def filter_by_type(self, db: Session, *, substring: str) -> Optional[list[TrainingRequestModel]]:
        return db.query(TrainingRequestModel).filter(func.lower(TrainingRequestModel.type).contains(substring.lower())).all()

    def filter_by_username(self, db: Session, *, substring: str) -> Optional[list[TrainingRequestModel]]:
        return db.query(TrainingRequestModel).join(UserModel).filter(func.lower(UserModel.username).contains(substring.lower())).all()

    def filter_by_user_fullname(self, db: Session, *, substring: str) -> Optional[list[TrainingRequestModel]]:
        return db.query(TrainingRequestModel).join(UserModel).filter(func.lower(UserModel.name).contains(substring.lower())).all()

    def filter_by_user_anyname(self, db: Session, *, substring: str) -> list[TrainingRequestModel]:

        result = []
        result.extend(self.filter_by_username(db, substring=substring))
        _search = self.filter_by_user_fullname(db, substring=substring)

        for row in _search:
            if row not in result:
                result.append(row)
        
        return result


trequest = CRUDTrainingRequest(TrainingRequestModel)