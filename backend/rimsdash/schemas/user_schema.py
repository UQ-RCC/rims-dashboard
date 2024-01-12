from typing import Optional, TypedDict, Dict, ForwardRef
from pydantic import root_validator

import rimsdash.config as config

from rimsdash.models import SystemRight

from .base_schema import BaseSchema

RIMS_URL = config.get('ppms', 'rims_url')

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


#export schema
#---------------
#   naming convention:  
#       out > info > refs > extended > full

class UserOutSchema(UserBaseSchema):
    """
    base export, no references
    """ 
    ...
    admin: bool = False

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
    admin: bool = False

    class Config:
        orm_mode = True

    #re-add root validator
    @root_validator
    def add_url(cls, values) -> str:
        if isinstance(values, dict) and 'userid' in values:
            values['url'] = f'{RIMS_URL}/user/?user={values.get("userid")}'
        return values


#Minimum for datatable search
class UserIdOnlyOutSchema(BaseSchema):
    """
    base with 

    WARNING: completely rebuilt from BaseSchema, not inherited
    """
    username: str
    name: str
    userid: int

    class Config:
        orm_mode = True


#Mnalysis schema

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