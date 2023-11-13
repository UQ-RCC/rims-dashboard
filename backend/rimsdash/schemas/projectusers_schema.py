from typing import Optional

from rimsdash.models import ProjectRight

from .base_schema import BaseSchema
from .user_schema import UserBaseSchema
from .project_schema import ProjectBaseSchema


class ProjectUsersBaseSchema(BaseSchema):
    username: str
    project_id: int
    status: ProjectRight  

class ProjectUsersCreateSchema(ProjectUsersBaseSchema):
    ...

class ProjectUsersUpdateSchema(ProjectUsersBaseSchema):
    ...

class ProjectUsersFullSchema(BaseSchema):
    ...
    user: UserBaseSchema = None
    system: ProjectBaseSchema = None
