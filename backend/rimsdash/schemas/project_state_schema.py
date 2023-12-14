from typing import Optional, ForwardRef

from .base_schema import BaseSchema

from rimsdash.models import IStatus


ProjectOutSchema=ForwardRef('ProjectOutSchema')
ProjectOutInfoSchema=ForwardRef('ProjectOutInfoSchema')


class ProjectStateBaseSchema(BaseSchema):
    project_id: int
    ok: IStatus = IStatus.disabled
    active: IStatus = IStatus.disabled
    billing: IStatus = IStatus.off
    ohs: IStatus = IStatus.disabled
    rdm: IStatus = IStatus.disabled
    phase: IStatus = IStatus.disabled
    ok_user: IStatus = IStatus.disabled

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


class ProjectStatePostProcessUpdateSchema(BaseSchema):
    project_id: int
    ok_user: IStatus

    class Config:
        orm_mode = True




ProjectStateOutInfoSchema.update_forward_refs()
ProjectStateOutFullRefsSchema.update_forward_refs()