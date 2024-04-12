from pydantic import Field
from datetime import datetime
from typing import Optional

from rimsdash.models import SyncType

from .base_schema import BaseSchema


class SyncBaseSchema(BaseSchema):
    id: Optional[int]

    class Config:
        orm_mode = True

class SyncCreateSchema(SyncBaseSchema):
    ...
    sync_type: SyncType
    start_time: datetime = Field(default_factory=datetime.now)
    complete: bool = False

class SyncCompleteSchema(SyncBaseSchema):
    ...
    id: int
    sync_type: SyncType
    end_time: datetime = Field(default_factory=datetime.now)
    complete: bool = True


class SyncOutSchema(SyncBaseSchema):
    ...
    id: int
    sync_type: SyncType
    start_time: datetime
    end_time: Optional[datetime]
    complete: bool = False