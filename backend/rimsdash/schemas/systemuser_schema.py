from typing import Optional, ForwardRef

from rimsdash.models import SystemRight

from .base_schema import BaseSchema

#use forward refs for circular deps

UserOutSchema = ForwardRef('UserOutSchema')
SystemOutSchema = ForwardRef('SystemOutSchema')
SystemOutInfoSchema = ForwardRef('SystemOutInfoSchema')

class SystemUserBaseSchema(BaseSchema):
    username: str
    system_id: int
    status: SystemRight

    class Config:
        orm_mode = True

class SystemUserFullSchema(BaseSchema):
    ...
    user: UserOutSchema = None
    system: SystemOutSchema = None

class SystemUserCreateSchema(SystemUserBaseSchema):
    ...

class SystemUserUpdateSchema(SystemUserBaseSchema):
    ...



#export schema
class SystemUserOutSchema(SystemUserBaseSchema):
    ...

class SystemUserOutInfoSchema(SystemUserBaseSchema):
    ...
    system: SystemOutSchema = None
    user: UserOutSchema = None

class SystemUserOutRefsFromUserSchema(SystemUserBaseSchema):
    """

    """    
    system: SystemOutInfoSchema = None

class SystemUserOutRefsFromSystemSchema(SystemUserBaseSchema):
    """

    """    
    user: SystemOutInfoSchema = None


#import the circular deps and update forward
from .user_schema import UserOutSchema
from .system_schema import SystemOutSchema, SystemOutInfoSchema

SystemUserOutInfoSchema.update_forward_refs()
SystemUserOutRefsFromUserSchema.update_forward_refs()
SystemUserOutRefsFromSystemSchema.update_forward_refs()

