from typing import Optional

from .base_schema import BaseSchema
from .system_schema import SystemBaseSchema
from .user_schema import UserBaseSchema

from rimsdash.models import AccessLevel

class SystemUserRightsBaseSchema(BaseSchema):
    username: str
    system_id: int
    access_level: AccessLevel

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
