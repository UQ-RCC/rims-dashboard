from typing import Optional, ForwardRef

from rimsdash.models import ProjectRight

from .base_schema import BaseSchema

#use forward refs for circular deps

UserOutSchema = ForwardRef('UserOutSchema')
UserOutWithStateSchema = ForwardRef('UserOutWithStateSchema')

ProjectOutSchema = ForwardRef('ProjectOutSchema')
ProjectOutWithStateSchema = ForwardRef('ProjectOutWithStateSchema')


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



#export schema
#---------------
#   naming convention:  
#       out > info > refs > extended > full

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




#import the circular deps and update forward
from .user_schema import UserOutSchema, UserOutWithStateSchema
from .project_schema import ProjectOutSchema, ProjectOutWithStateSchema

#update local schema with refs
ProjectUsersFullSchema.update_forward_refs()

ProjectUsersOutFromUserSchema.update_forward_refs()
ProjectUsersOutFromProjectSchema.update_forward_refs()