from typing import Optional, TypedDict, Dict, ForwardRef
from pydantic import root_validator, Field

import rimsdash.config as config

from rimsdash.models import SystemRight, AdminRight

from .base_schema import BaseSchema

RIMS_URL = config.get('ppms', 'rims_url', required=True)

# forward refs to other schemas
UserStateOutSchema=ForwardRef('UserStateOutSchema')
ProjectUsersWithProjectSchema=ForwardRef('ProjectUsersWithProjectSchema')
SystemUserOutInfoSchema=ForwardRef('SystemUserOutInfoSchema')
SystemUserOutSchema = ForwardRef('SystemUserOutSchema')
ProjectUsersOutSchema = ForwardRef('ProjectUsersOutSchema')

class UserBaseSchema(BaseSchema):
    username: str
    name: str
    userid: Optional[int]
    email: str
    group: str
    active: bool

    class Config:
        orm_mode = True



# Properties on creation
class UserCreateSchema(UserBaseSchema):
    userid: int
    ...

# Properties on update
class UserUpdateSchema(UserBaseSchema):
    userid: int    
    ...

class UserReceiveSchema(UserBaseSchema):
    userid: int    
    ...

# Properties on update
class UserUpdateAdminSchema(BaseSchema):
    admin: AdminRight

    class Config:
        orm_mode = True

class UserReceiveSchema(UserBaseSchema):
    ...


# return schema

class UserReturnAdminSchema(BaseSchema):
    admin: AdminRight = AdminRight.none

    class Config:
        orm_mode = True


#export schema
#---------------
#   naming convention:  
#       out > info > refs > extended > full

class UserOutSchema(UserBaseSchema):
    """
    base export, no references
    """ 
    ...
    admin: Optional[AdminRight] = AdminRight.none

    #use root_validator to add a computed property that will return via .dict() & .json()
    #   @property is cleaner for direct access only
    @root_validator
    def add_url(cls, values) -> str:
        if isinstance(values, dict) and 'userid' in values:
            values['url'] = f'{RIMS_URL}/user/?user={values.get("userid")}'
        return values
        #   NB: operate via values dict rather than on self directly

class UserOutWithStateSchema(UserOutSchema):
    """

    FUTURE: consider merging this with UserOutSchema 
        and creating UserNoRefs for base only
    """
    ...
    user_state: Optional[UserStateOutSchema]

class UserOutWithProjectRightsSchema(UserOutSchema):
    """

    FUTURE: consider merging this with UserOutSchema 
        and creating UserNoRefs for base only
    """
    ...
    project_rights: Optional[list[ProjectUsersWithProjectSchema]]

class UserOutRefsSchema(UserOutSchema):
    """
    include projects w/ state, and systems
    """
    ...
    user_state: Optional[UserStateOutSchema]
    system_rights: Optional[list[SystemUserOutInfoSchema]]
    project_rights: Optional[list[ProjectUsersWithProjectSchema]]


#Minimum for table
class UserMinOutSchema(BaseSchema):
    """
    base with admin, no email

    WARNING: completely rebuilt from BaseSchema, not inherited
    """
    username: str
    name: str
    userid: int
    group: str
    active: bool
    admin: Optional[AdminRight] = AdminRight.none

    class Config:
        orm_mode = True

    #re-add root validator
    @root_validator
    def add_url(cls, values) -> str:
        if isinstance(values, dict) and 'userid' in values:
            values['url'] = f'{RIMS_URL}/user/?user={values.get("userid")}'
        return values

#-------------------------------------
#Rebuilt from BaseSchema:

class UserIdOnlyOutSchema(BaseSchema):
    """
    Minimum for datatable search
    """
    username: str
    name: str
    userid: int

    class Config:
        orm_mode = True

class UserSelfOutSchema(BaseSchema):
    """
    base info level for non-admin user accessing self
    """     
    username: str
    name: str
    userid: Optional[int]
    email: str
    active: bool
    admin: AdminRight = AdminRight.none

    class Config:
        orm_mode = True

class UserAdminOutSchema(BaseSchema):
    """
    returns admin status only
    """
    admin: AdminRight = AdminRight.none
    
    class Config:
        orm_mode = True

#-------------------------------------
#Analysis schema
class UserForStateCheckSchema(UserOutSchema):
    """
    """
    ...
    user_state: Optional[UserStateOutSchema]
    system_rights: Optional[list[SystemUserOutInfoSchema]]
    project_rights: Optional[list[ProjectUsersWithProjectSchema]]



#import the circular deps and update forward
from .systemuser_schema import SystemUserOutSchema, SystemUserOutInfoSchema
from .projectusers_schema import ProjectUsersOutSchema, ProjectUsersWithProjectSchema
from .user_state_schema import UserStateOutSchema

#update local schema with refs
UserOutWithStateSchema.update_forward_refs()
UserOutRefsSchema.update_forward_refs()
UserOutWithProjectRightsSchema.update_forward_refs()
UserForStateCheckSchema.update_forward_refs()




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