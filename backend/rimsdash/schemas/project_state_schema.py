from typing import Optional

from .base_schema import BaseSchema

from rimsdash.models import IStatus

class ProjectStateBaseSchema(BaseSchema):
    id: int
    ok: IStatus = IStatus.off
    active: IStatus = IStatus.off
    billing: IStatus = IStatus.off
    ohs: IStatus = IStatus.off
    rdm: IStatus = IStatus.off
    phase: IStatus = IStatus.off

    class Config:
        orm_mode = True

class ProjectStateCreateSchema(ProjectStateBaseSchema):
    ...

class ProjectStateUpdateSchema(ProjectStateBaseSchema):
    ...