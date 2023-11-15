from typing import Optional, ForwardRef

from rimsdash.models import ProjectRight

from .base_schema import BaseSchema

#use forward refs for circular deps
UserBaseSchema = ForwardRef('UserBaseSchema')
ProjectBaseSchema = ForwardRef('ProjectBaseSchema')

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

class ProjectUsersFullSchema(BaseSchema):
    ...
    user: UserBaseSchema = None
    project: ProjectBaseSchema = None

#import the circular deps and update forward
from .user_schema import UserBaseSchema
from .project_schema import ProjectBaseSchema

ProjectUsersFullSchema.update_forward_refs()