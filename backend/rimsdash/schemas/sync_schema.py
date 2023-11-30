from datetime import datetime

from rimsdash.models.sync_models import SyncType

from .base_schema import BaseSchema


class SyncBaseSchema(BaseSchema):
    id: int

    class Config:
        orm_mode = True

class SyncCreateSchema(SyncBaseSchema):
    id: int
    sync_type: SyncType
    start_time: datetime
    complete: bool = False

class SyncCompleteSchema(SyncBaseSchema):
    id: int
    sync_type: SyncType    
    end_time: datetime
    complete: bool = True