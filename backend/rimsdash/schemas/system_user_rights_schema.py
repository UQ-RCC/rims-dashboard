from typing import Optional

from rimsdash.models import SystemRight

from .base_schema import BaseSchema
from .system_schema import SystemBaseSchema
from .user_schema import UserBaseSchema

class SystemUserRightsBaseSchema(BaseSchema):
    username: str
    system_id: int
    status: SystemRight

    class Config:
        orm_mode = True

class SystemUserRightsCreateSchema(SystemUserRightsBaseSchema):
    ...

class SystemUserRightsUpdateSchema(SystemUserRightsBaseSchema):
    ...

class SystemUserRightsFullSchema(BaseSchema):
    ...
    user: UserBaseSchema = None
    system: SystemBaseSchema = None
