from typing import Optional

from sqlalchemy.orm import Session

from rimsdash.crud.base_crud import CRUDBase
from rimsdash.models.trequest_models import TrainingRequestModel
from rimsdash.schemas.trequest_schema import TrainingRequestCreateSchema, TrainingRequestUpdateSchema

class CRUDTrainingRequest(CRUDBase[TrainingRequestModel, TrainingRequestCreateSchema, TrainingRequestUpdateSchema]):
    ...

trequest = CRUDTrainingRequest(TrainingRequestModel)