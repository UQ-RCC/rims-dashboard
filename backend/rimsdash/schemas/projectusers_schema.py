from typing import Optional, ForwardRef

from rimsdash.models import ProjectRight

from .base_schema import BaseSchema

#use forward refs for circular deps

UserOutSchema = ForwardRef('UserOutSchema')
UserOutInfoSchema = ForwardRef('UserOutInfoSchema')
UserOutWithStateSchema = ForwardRef('UserOutWithStateSchema')

ProjectOutSchema = ForwardRef('ProjectOutSchema')
ProjectOutInfoSchema = ForwardRef('ProjectOutInfoSchema')
ProjectOutRefsSchema = ForwardRef('ProjectOutRefsSchema')
ProjectOutWithStateSchema = ForwardRef('ProjectOutWithStateSchema')

ProjectOutRefsFromUserSchema = ForwardRef('ProjectOutRefsFromUserSchema')

class ProjectUsersBaseSchema(BaseSchema):
    username: str
    project_id: int
    status: ProjectRight  

    class Config:
        orm_mode = True


class ProjectUsersCreateSchema(ProjectUsersBaseSchema):
    ...

class ProjectUsersUpdateSchema(ProjectUsersBaseSchema):
    ...

class ProjectUsersFullSchema(ProjectUsersBaseSchema):
    ...
    user: UserOutSchema = None
    project: ProjectOutSchema = None



#--------------------
#export schema
class ProjectUsersOutSchema(ProjectUsersBaseSchema):
    """
    No references, terminates recursion
    """    
    ...

class ProjectUsersOutFromProjectSchema(ProjectUsersBaseSchema):
    """
    Include linked users with states
    """    
    ...
    user: UserOutWithStateSchema = None

class ProjectUsersOutFromUserSchema(ProjectUsersBaseSchema):
    """
    Include linked projects with states
    """    
    ...    
    project: ProjectOutWithStateSchema = None






class ProjectUsersOutInfoSchema(ProjectUsersBaseSchema):
    """
    No references, terminates recursion
    """    
    ...    
    user: UserOutSchema = None
    project: ProjectOutSchema = None


class ProjectUsersOutRefsFromProjectSchema(ProjectUsersBaseSchema):
    """
    References terminating schema only
    """     
    ...
    user: UserOutInfoSchema = None


#recursion-handling
class ProjectUsersOutRefsFromUserSchema(ProjectUsersBaseSchema):
    """
    References terminating schema only
    """
    ...
    project: ProjectOutRefsSchema = None






#import the circular deps and update forward
from .user_schema import UserOutSchema, UserOutInfoSchema, UserOutWithStateSchema
from .project_schema import ProjectOutSchema, ProjectOutInfoSchema, ProjectOutRefsSchema, ProjectOutWithStateSchema

#update local schema with refs
ProjectUsersFullSchema.update_forward_refs()
ProjectUsersOutInfoSchema.update_forward_refs()
ProjectUsersOutRefsFromProjectSchema.update_forward_refs()
ProjectUsersOutRefsFromUserSchema.update_forward_refs()

ProjectUsersOutFromUserSchema.update_forward_refs()
ProjectUsersOutFromProjectSchema.update_forward_refs()