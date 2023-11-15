from typing import Optional, ForwardRef

from rimsdash.models import SystemRight

from .base_schema import BaseSchema

#use forward refs for circular deps
UserTerminalSchema = ForwardRef('UserTerminalSchema')
SystemTerminalSchema = ForwardRef('SystemTerminalSchema')

class SystemUserRightsBaseSchema(BaseSchema):
    username: str
    system_id: int
    status: SystemRight

    class Config:
        orm_mode = True

class SystemUserRightsFullSchema(BaseSchema):
    ...
    user: UserTerminalSchema = None
    system: SystemTerminalSchema = None

class SystemUserRightsCreateSchema(SystemUserRightsBaseSchema):
    ...

class SystemUserRightsUpdateSchema(SystemUserRightsBaseSchema):
    ...


#export schema
class SystemUserRightsTerminalSchema(SystemUserRightsBaseSchema):
    ...

class SystemUserRightsTerminatingSchema(SystemUserRightsBaseSchema):
    """
    References terminal schema only
    """    
    user: UserTerminalSchema = None
    system: SystemTerminalSchema = None


#import the circular deps and update forward
from .user_schema import UserTerminalSchema
from .system_schema import SystemTerminalSchema

SystemUserRightsFullSchema.update_forward_refs()
SystemUserRightsTerminatingSchema.update_forward_refs()

