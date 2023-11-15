from typing import Optional, ForwardRef

from rimsdash.models import ProjectRight

from .base_schema import BaseSchema

#use forward refs for circular deps
UserTerminatingSchema = ForwardRef('UserTerminatingSchema')
ProjectTerminatingSchema = ForwardRef('ProjectTerminatingSchema')
UserTerminalSchema = ForwardRef('UserTerminalSchema')
ProjectTerminalSchema = ForwardRef('ProjectTerminalSchema')

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
    user: UserTerminatingSchema = None
    project: ProjectTerminatingSchema = None


#export schema
class ProjectUsersTerminalSchema(ProjectUsersBaseSchema):
    """
    No references, terminates recursion
    """    
    ...

class ProjectUsersTerminatingSchema(ProjectUsersBaseSchema):
    """
    References terminal schema only
    """     
    ...
    user: UserTerminalSchema = None
    project: ProjectTerminalSchema = None

if False:
    class ProjectUsersPreTerminatingSchema(ProjectUsersBaseSchema):
        """
        References terminating schema only
        """     
        ...
        user: UserTerminatingSchema = None
        project: ProjectTerminatingSchema = None

    
class ProjectUsersTerminatingFromProjectSchema(ProjectUsersBaseSchema):
    """
    References terminating schema only
    """     
    ...
    user: UserTerminatingSchema = None

class ProjectUsersTerminatingFromUserSchema(ProjectUsersBaseSchema):
    """
    References terminating schema only
    """
    ...
    project: ProjectTerminatingSchema = None


#import the circular deps and update forward
from .user_schema import UserTerminatingSchema, UserTerminalSchema
from .project_schema import ProjectTerminatingSchema, ProjectTerminalSchema

#update local schema with refs
ProjectUsersFullSchema.update_forward_refs()
ProjectUsersTerminatingSchema.update_forward_refs()
ProjectUsersTerminatingFromProjectSchema.update_forward_refs()
ProjectUsersTerminatingFromUserSchema.update_forward_refs()