from typing import Optional, ForwardRef

from .base_schema import BaseSchema

#use forward refs for circular deps
ProjectUsersBaseSchema = ForwardRef('ProjectUsersBaseSchema')

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

# Properties on creation
class ProjectCreateSchema(ProjectBaseSchema):
    ...

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


class ProjectFullSchema(ProjectBaseSchema):
    qcollection: Optional[str] = None
    status: Optional[str] = None
    users: Optional[list[ProjectUsersBaseSchema]] = []
    ...


#import the circular deps and update forward
from .projectusers_schema import ProjectUsersBaseSchema
ProjectFullSchema.update_forward_refs()