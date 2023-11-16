from typing import Optional, ForwardRef

from rimsdash.models import SystemRight

from .base_schema import BaseSchema

#use forward refs for circular deps

UserOutSchema = ForwardRef('UserOutSchema')
SystemOutSchema = ForwardRef('SystemOutSchema')

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
#---------------
#   naming convention:  
#       out > info > refs > extended > full

class SystemUserOutSchema(SystemUserBaseSchema):
    ...

class SystemUserOutInfoSchema(SystemUserBaseSchema):
    ...
    system: SystemOutSchema = None
    user: UserOutSchema = None




#import the circular deps and update forward
from .user_schema import UserOutSchema
from .system_schema import SystemOutSchema

SystemUserOutInfoSchema.update_forward_refs()


