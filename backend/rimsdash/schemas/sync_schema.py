from pydantic import Field
from datetime import datetime
from typing import Optional

from rimsdash.models import SyncType, SyncStatus

from .base_schema import BaseSchema


class SyncBaseSchema(BaseSchema):
    id: Optional[int]

    class Config:
        orm_mode = True

class SyncCreateSchema(SyncBaseSchema):
    ...
    sync_type: SyncType
    start_time: datetime = Field(default_factory=datetime.now)
    status: SyncStatus = SyncStatus.in_progress

class SyncCompleteSchema(SyncBaseSchema):
    ...
    id: int
    sync_type: SyncType
    end_time: datetime = Field(default_factory=datetime.now)
    status: SyncStatus = SyncStatus.complete


class SyncOutSchema(SyncBaseSchema):
    ...
    id: int
    sync_type: SyncType
    start_time: datetime
    end_time: Optional[datetime]
    status: SyncStatus