from typing import Optional, ForwardRef

from rimsdash.models import SystemRight

from .base_schema import BaseSchema

#use forward refs for circular deps
SystemBaseSchema = ForwardRef('SystemBaseSchema')
UserBaseSchema = ForwardRef('UserBaseSchema')

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


#import the circular deps and update forward
from .system_schema import SystemBaseSchema
from .user_schema import UserBaseSchema

SystemUserRightsFullSchema.update_forward_refs()

