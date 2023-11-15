from typing import Optional, ForwardRef

from .base_schema import BaseSchema

#use forward refs for circular deps
ProjectStateTerminalSchema = ForwardRef('ProjectStateTerminalSchema')

ProjectUsersTerminalSchema = ForwardRef('ProjectUsersTerminalSchema')
ProjectUsersTerminatingSchema = ForwardRef('ProjectUsersTerminatingSchema')
ProjectUsersTerminatingFromProjectSchema = ForwardRef('ProjectUsersTerminatingFromProjectSchema')

class ProjectBaseSchema(BaseSchema):
    id: int
    title: str
    phase: int
    active: bool = False   
    type: str
    group: str
    coreid: int = 2    
    bcode: str = None
    affiliation: str = None
    description: str = None

    class Config:
        orm_mode = True

#complete DB schema with all fields
class ProjectFullSchema(ProjectBaseSchema):
    qcollection: Optional[str] = None
    status: Optional[str] = None
    project_state: Optional[list[ProjectStateTerminalSchema]]
    user_rights: Optional[list[ProjectUsersTerminatingSchema]]
    ...


# Properties on creation
class ProjectCreateSchema(ProjectBaseSchema):
    ...

# Additional properties on initialise
class ProjectInitDetailsSchema(BaseSchema):
    id: int
    qcollection: str = None
    status: str = None

    class Config:
        orm_mode = True

# Properties on update
class ProjectUpdateSchema(ProjectBaseSchema):
    ...

class ProjectReceiveSchema(ProjectBaseSchema):
    ...    



#export schema
class ProjectTerminalSchema(ProjectBaseSchema):
    """
    No references, terminates recursion
    """    
    ...
    id: int
    qcollection: str = None
    status: str = None

class ProjectTerminatingSchema(ProjectBaseSchema):
    """
    References terminal schema only
    """ 
    ...
    qcollection: Optional[str] = None
    status: Optional[str] = None
    project_state: Optional[list[ProjectStateTerminalSchema]]    
    user_rights: Optional[list[ProjectUsersTerminalSchema]]    

class ProjectPreTerminatingSchema(ProjectBaseSchema):
    """
    References terminating schema only
    """ 
    ...
    qcollection: Optional[str] = None
    status: Optional[str] = None
    project_state: Optional[list[ProjectStateTerminalSchema]]    
    user_rights: Optional[list[ProjectUsersTerminatingFromProjectSchema]]



#import the circular deps and update forward
from .projectusers_schema import ProjectUsersTerminalSchema, ProjectUsersTerminatingSchema, ProjectUsersTerminatingFromProjectSchema
from .project_state_schema import ProjectStateTerminalSchema

ProjectFullSchema.update_forward_refs()
ProjectTerminatingSchema.update_forward_refs()
ProjectPreTerminatingSchema.update_forward_refs()
