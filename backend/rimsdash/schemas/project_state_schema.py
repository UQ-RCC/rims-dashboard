from typing import Optional, ForwardRef

from .base_schema import BaseSchema

from rimsdash.models import IStatus


ProjectOutSchema=ForwardRef('ProjectOutSchema')
ProjectOutInfoSchema=ForwardRef('ProjectOutInfoSchema')


class ProjectStateBaseSchema(BaseSchema):
    project_id: int
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


class ProjectStateOutSchema(ProjectStateBaseSchema):
    """
    No onward references, terminates recursion
    """
    ...

class ProjectStateOutInfoSchema(ProjectStateBaseSchema):
    """
    No onward references, terminates recursion
    """
    project: ProjectOutSchema


class ProjectStateOutFullRefsSchema(ProjectStateBaseSchema):
    """
    No onward references, terminates recursion
    """
    project: ProjectOutInfoSchema


ProjectStateOutInfoSchema.update_forward_refs()
ProjectStateOutFullRefsSchema.update_forward_refs()