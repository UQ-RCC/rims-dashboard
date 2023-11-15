from typing import Optional, TypedDict, Dict, ForwardRef

from rimsdash.models import SystemRight

from .base_schema import BaseSchema

#use forward refs for circular deps
SystemUserRightsTerminalSchema = ForwardRef('SystemUserRightsTerminalSchema')
UserStateTerminalSchema = ForwardRef('UserStateTerminalSchema')
ProjectUsersTerminalSchema = ForwardRef('ProjectUsersTerminalSchema')
ProjectUsersTerminatingSchema = ForwardRef('ProjectUsersTerminatingSchema')
ProjectUsersTerminatingFromUserSchema = ForwardRef('ProjectUsersTerminatingFromUserSchema')

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
    ...
    admin: bool = False
    user_state: Optional[list[UserStateTerminalSchema]]
    system_rights: Optional[list[SystemUserRightsTerminalSchema]]
    project_rights: Optional[list[ProjectUsersTerminatingSchema]]


# Properties on creation
class UserCreateSchema(UserBaseSchema):
    userid: int
    ...

# Properties on update
class UserUpdateSchema(UserBaseSchema):
    ...

class UserReceiveSchema(UserBaseSchema):
    ...

#export schema

class UserTerminalSchema(UserBaseSchema):
    """
    References terminal schema only
    """
    ...
    admin: bool = False

class UserTerminatingSchema(UserBaseSchema):
    """
    References terminal schema only
    """    
    ...
    admin: bool = False
    user_state: Optional[list[UserStateTerminalSchema]]
    system_rights: Optional[list[SystemUserRightsTerminalSchema]]
    project_rights: Optional[list[ProjectUsersTerminalSchema]]

class UserPreTerminatingSchema(UserBaseSchema):
    """
    References terminating schema only
    """    
    ...
    admin: bool = False
    user_state: Optional[list[UserStateTerminalSchema]]
    system_rights: Optional[list[SystemUserRightsTerminalSchema]]
    project_rights: Optional[list[ProjectUsersTerminatingFromUserSchema]]


#import the circular deps and update forward
from .system_user_rights_schema import SystemUserRightsTerminalSchema
from .projectusers_schema import ProjectUsersTerminalSchema, ProjectUsersTerminatingSchema, ProjectUsersTerminatingFromUserSchema
from .user_state_schema import UserStateTerminalSchema

#update local schema with refs
UserFullSchema.update_forward_refs()
UserTerminatingSchema.update_forward_refs()
UserPreTerminatingSchema.update_forward_refs()