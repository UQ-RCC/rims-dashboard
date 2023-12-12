from typing import Optional, ForwardRef

from .base_schema import BaseSchema

# forward refs to other schemas
ProjectStateOutSchema=ForwardRef('ProjectStateOutSchema')
ProjectUsersOutSchema=ForwardRef('ProjectUsersOutSchema')
ProjectUsersOutUserMin=ForwardRef('ProjectUsersOutUserMin')
ProjectUsersWithUserSchema=ForwardRef('ProjectUsersWithUserSchema')
ProjectAccountOutSchema=ForwardRef('ProjectAccountOutSchema')

class ProjectBaseSchema(BaseSchema):
    id: int
    title: str
    phase: int
    active: bool = False   
    type: str
    group: str
    coreid: int = 2    
    affiliation: str = None
    description: str = None

    class Config:
        orm_mode = True


# Properties on creation
class ProjectCreateSchema(ProjectBaseSchema):
    ...

class ProjectReceiveSchema(ProjectCreateSchema):
    ...

# Additional properties on initialise
class ProjectInitDetailsSchema(BaseSchema):
    id: int
    qcollection: str = None
    status: str = None

    class Config:
        orm_mode = True

#RIMS translation check
class ProjectListTranslateSchema(ProjectReceiveSchema):
    bcode: str
    ...


# Properties on update
class ProjectUpdateSchema(ProjectBaseSchema):
    ...


# Secondary receive
    
class ProjectFromAccountSchema(BaseSchema):
    id: int
    title: str
    active: bool = False           
    group: str

    class Config:
        orm_mode = True    







#export schema
#---------------
#   naming convention:  
#       out > info > refs > extended > full


class ProjectOutSchema(ProjectBaseSchema):
    """
    base export, no references
    """    
    ...
    qcollection: str = None
    status: str = None

class ProjectOutWithStateSchema(ProjectOutSchema):
    """

    FUTURE: consider merging this with ProjectOutSchema 
        and creating ProjectNoRefs for ProjectStateSchema only
    """
    ...
    project_state: Optional[list[ProjectStateOutSchema]]

class ProjectOutRefsSchema(ProjectOutSchema):
    """
    include users and user state
    """ 
    ...
    project_state: Optional[list[ProjectStateOutSchema]]    
    user_rights: Optional[list[ProjectUsersWithUserSchema]]  
    project_account: Optional[list[ProjectAccountOutSchema]]

#Minimum for table
class ProjectMinOutSchema(BaseSchema):
    id: int
    title: str
    group: str
    coreid: int = 2
    affiliation: str = None

    class Config:
        orm_mode = True


class ProjectOutRefsMinSchema(ProjectMinOutSchema):
    """

    """
    ...
    project_state: Optional[list[ProjectStateOutSchema]]
    user_rights: Optional[list[ProjectUsersOutUserMin]]
    project_account: Optional[list[ProjectAccountOutSchema]]



class ProjectForStateCheckSchema(ProjectOutSchema):
    """
    """
    ...
    project_state: Optional[list[ProjectStateOutSchema]]    
    user_rights: Optional[list[ProjectUsersWithUserSchema]]  
    project_account: Optional[list[ProjectAccountOutSchema]]



#import the circular deps and update forward
from .projectusers_schema import ProjectUsersOutSchema, ProjectUsersWithUserSchema, ProjectUsersOutUserMin
from .project_state_schema import ProjectStateOutSchema
from .projectaccount_schema import ProjectAccountOutSchema


ProjectOutWithStateSchema.update_forward_refs()
ProjectOutRefsSchema.update_forward_refs()
ProjectOutRefsMinSchema.update_forward_refs()
ProjectForStateCheckSchema.update_forward_refs()