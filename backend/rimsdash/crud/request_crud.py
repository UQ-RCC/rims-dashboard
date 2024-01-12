from typing import Optional

from sqlalchemy.orm import Session

from rimsdash.crud.base_crud import CRUDBase
from rimsdash.models.request_models import TrainingRequestModel
from rimsdash.schemas.request_schema import TrainingRequestCreateSchema, TrainingRequestUpdateSchema

class CRUDTrainingRequest(CRUDBase[TrainingRequestModel, TrainingRequestCreateSchema, TrainingRequestUpdateSchema]):
    ...

request = CRUDTrainingRequest(TrainingRequestModel)