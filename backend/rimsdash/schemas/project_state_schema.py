from typing import Optional, ForwardRef

from .base_schema import BaseSchema

from rimsdash.models import IStatus


ProjectOutSchema=ForwardRef('ProjectOutSchema')
ProjectOutInfoSchema=ForwardRef('ProjectOutInfoSchema')


class ProjectStateBaseSchema(BaseSchema):
    project_id: int
    ok: IStatus = IStatus.none
    active: IStatus = IStatus.none
    billing: IStatus = IStatus.none
    ohs: IStatus = IStatus.none
    rdm: IStatus = IStatus.none
    phase: IStatus = IStatus.none
    ok_user: IStatus = IStatus.none

    class Config:
        orm_mode = True

class ProjectStateCreateSchema(ProjectStateBaseSchema):
    ...

class ProjectStateUpdateSchema(ProjectStateBaseSchema):
    ...

class ProjectStateReceiveSchema(ProjectStateBaseSchema):
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
    ok_user: IStatus = IStatus.none

    class Config:
        orm_mode = True




ProjectStateOutInfoSchema.update_forward_refs()
ProjectStateOutFullRefsSchema.update_forward_refs()