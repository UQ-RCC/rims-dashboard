from typing import Optional

from pydantic import BaseModel

from .userproject_schema import UserProjectBaseSchema

class ProjectBaseSchema(BaseModel):
    id: int
    title: str
    type: str
    phase: int
    description: Optional[str] = None
    qcollection: Optional[str] = None
    coreid: int = 2
    #bcode = Optional[str] = None
    users: list[UserProjectBaseSchema] = []
    active: bool = False
    class Config:
        orm_mode = True

# Properties on creation
class ProjectCreateSchema(ProjectBaseSchema):
    ...

# Properties on update
class ProjectUpdateSchema(ProjectBaseSchema):
    ...

