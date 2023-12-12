from typing import Optional, ForwardRef

from rimsdash.models import ProjectRight

from .base_schema import BaseSchema

# forward refs to other schemas
UserOutSchema = ForwardRef('UserOutSchema')
UserMinOutSchema = ForwardRef('UserMinOutSchema')
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

class ProjectUsersWithUserSchema(ProjectUsersBaseSchema):
    """
    Include linked users with states
    """    
    ...
    user: UserOutWithStateSchema = None

class ProjectUsersWithProjectSchema(ProjectUsersBaseSchema):
    """
    Include linked projects with states
    """    
    ...    
    project: ProjectOutWithStateSchema = None


class ProjectUsersOutUserMin(ProjectUsersBaseSchema):
    """
    Include linked users with minimum info
    """    
    ...
    user: UserMinOutSchema = None




#import the circular deps and update forward
from .user_schema import UserOutSchema, UserOutWithStateSchema, UserMinOutSchema
from .project_schema import ProjectOutSchema, ProjectOutWithStateSchema

#update local schema with refs

ProjectUsersFullSchema.update_forward_refs()
ProjectUsersWithProjectSchema.update_forward_refs()
ProjectUsersWithUserSchema.update_forward_refs()
ProjectUsersOutUserMin.update_forward_refs()