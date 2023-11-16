from typing import Optional, TypedDict, Dict, ForwardRef

from rimsdash.models import SystemRight

from .base_schema import BaseSchema

#use forward refs for circular deps

#NEW
UserStateOutSchema=ForwardRef('UserStateOutSchema')
ProjectUsersOutSchema=ForwardRef('ProjectUsersOutSchema')
ProjectUsersOutFromUserSchema=ForwardRef('ProjectUsersOutFromUserSchema')
ProjectUsersOutInfoSchema=ForwardRef('ProjectUsersOutInfoSchema')
ProjectUsersOutRefsFromUserSchema=ForwardRef('ProjectUsersOutRefsFromUserSchema')
SystemUserOutSchema=ForwardRef('SystemUserOutSchema')
SystemUserOutInfoSchema=ForwardRef('SystemUserOutInfoSchema')

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
    admin: Optional[bool]
    user_state: Optional[list[UserStateOutSchema]]
    system_rights: Optional[list[SystemUserOutSchema]]
    project_rights: Optional[list[ProjectUsersOutInfoSchema]]


# Properties on creation
class UserCreateSchema(UserBaseSchema):
    userid: int
    ...

# Properties on update
class UserUpdateSchema(UserBaseSchema):
    ...

# Properties on update
class UserUpdateAdminSchema(BaseSchema):
    admin: Optional[bool]

    class Config:
        orm_mode = True

class UserReceiveSchema(UserBaseSchema):
    ...


# return schema

class UserReturnAdminSchema(BaseSchema):
    admin: bool = False

    class Config:
        orm_mode = True


#export schema NEW

class UserOutSchema(UserBaseSchema):
    """
    base export, no references
    """ 
    ...
    admin: bool = False


class UserOutWithStateSchema(UserOutSchema):
    """

    FUTURE: consider merging this with ProjectOutSchema 
        and creating ProjectNoRefs for ProjectStateSchema only
    """
    ...
    user_state: Optional[list[UserStateOutSchema]]


class UserOutInfoSchema(UserOutSchema):
    """
    UNUSED
    """
    ...
    user_state: Optional[list[UserStateOutSchema]]
    system_rights: Optional[list[SystemUserOutSchema]]
    project_rights: Optional[list[ProjectUsersOutSchema]]

class UserOutRefsSchema(UserOutSchema):
    """
    include projects w/ state, and systems
    """
    ...
    user_state: Optional[list[UserStateOutSchema]]
    system_rights: Optional[list[SystemUserOutInfoSchema]]
    project_rights: Optional[list[ProjectUsersOutFromUserSchema]]


class UserOutExtendedRefsSchema(UserOutSchema):
    """
    UNUSED
    """
    ...
    user_state: Optional[list[UserStateOutSchema]]
    system_rights: Optional[list[SystemUserOutInfoSchema]]
    project_rights: Optional[list[ProjectUsersOutInfoSchema]]



#import the circular deps and update forward
from .systemuser_schema import SystemUserOutSchema, SystemUserOutInfoSchema
from .projectusers_schema import ProjectUsersOutSchema, ProjectUsersOutInfoSchema, ProjectUsersOutFromUserSchema
from .user_state_schema import UserStateOutSchema

#update local schema with refs
UserFullSchema.update_forward_refs()
UserOutWithStateSchema.update_forward_refs()
UserOutInfoSchema.update_forward_refs()
UserOutRefsSchema.update_forward_refs()
UserOutExtendedRefsSchema.update_forward_refs()


"""
MOCK 

Info only

Info + State

Info + State + project rights

Info + State + project rights + project info

---------------------

UserData
	#eg. user info
	
UserDataWithRefs
	#eg. user info
	#	+ user-project-rights*
	#	+ user-system-rights*    
	#	+ user-state*

UserDataWithExtendedRefs
	#eg. user info
	#	+ user-project-rights
	#		+ project info*
	#	+ user-system-rights
    #       + system info*
	#	+ user-state*

UserDataWithFullRefs
	#	+ user-project-rights
	#		+ project info
	#			+ project-user-rights
	#				+user info*
	#			+ project-state*
	#	+ user-system-rights
    #       + system info*    
	#	+ user-state*


UserStateExport
    # user_state
    #   + user
    #	    + user-project-rights
    #		    + project info
    #			    + project-user-rights
    #				    +user info*
    #       		+ project-state*
    
    

"""