from typing import Optional

from .base_schema import BaseSchema

from .userproject_schema import UserProjectBaseSchema

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
    users: Optional[list[UserProjectBaseSchema]] = []
    ...
