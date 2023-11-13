from typing import Optional, TypedDict, Dict, ForwardRef

from rimsdash.models import SystemRight

from .base_schema import BaseSchema

#use forward refs for circular deps
SystemUserRightsBaseSchema = ForwardRef('SystemUserRightsBaseSchema')
ProjectUsersBaseSchema = ForwardRef('ProjectUsersBaseSchema')

class UserBaseSchema(BaseSchema):
    username: str
    name: str
    userid: Optional[int]
    email: str
    group: str
    active: bool

    class Config:
        orm_mode = True

#complete DB schema with all fields
class UserFullSchema(UserBaseSchema):
    username: str
    name: str
    userid: Optional[int]
    email: str
    group: str
    active: bool
    admin: bool = False
    system_rights: Optional[list[SystemUserRightsBaseSchema]]
    projects: Optional[list[ProjectUsersBaseSchema]] = []

# Properties on creation
class UserCreateSchema(UserBaseSchema):
    userid: int
    ...

# Properties on update
class UserUpdateSchema(UserBaseSchema):
    ...

class UserReceiveSchema(UserBaseSchema):
    ...


#import the circular deps and update forward
from .system_user_rights_schema import SystemUserRightsBaseSchema
from .projectusers_schema import ProjectUsersBaseSchema
UserFullSchema.update_forward_refs()