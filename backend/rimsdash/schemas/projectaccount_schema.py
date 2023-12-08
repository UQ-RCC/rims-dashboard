from typing import Optional, ForwardRef

from .base_schema import BaseSchema

#use forward refs for circular deps

ProjectOutSchema = ForwardRef('ProjectOutSchema')
AccountOutSchema = ForwardRef('AccountOutSchema')

class ProjectAccountBaseSchema(BaseSchema):
    bcode: int
    project_id: int
    valid: bool

    class Config:
        orm_mode = True


class ProjectAccountReceiveSchema(ProjectAccountBaseSchema):
    ...


class ProjectAccountUpdateSchema(ProjectAccountBaseSchema):
    ...


#export schema
#---------------
#   naming convention:  
#       out > info > refs > extended > full

class ProjectAccountOutSchema(ProjectAccountBaseSchema):
    ...

class ProjectAccountOutInfoSchema(ProjectAccountBaseSchema):
    ...
    project: ProjectOutSchema = None
    account: AccountOutSchema = None

from .account_schema import AccountOutSchema
from .project_schema import ProjectOutSchema
ProjectAccountOutInfoSchema.update_forward_refs()