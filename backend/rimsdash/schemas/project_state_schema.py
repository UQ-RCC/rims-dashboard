from typing import Optional, ForwardRef

from .base_schema import BaseSchema

from rimsdash.models import IStatus


ProjectOutSchema=ForwardRef('ProjectOutSchema')
ProjectOutInfoSchema=ForwardRef('ProjectOutInfoSchema')


class ProjectStateBaseSchema(BaseSchema):
    project_id: int
    active: IStatus = IStatus.none
    billing: IStatus = IStatus.none
    ohs: IStatus = IStatus.none
    rdm: IStatus = IStatus.none
    phase: IStatus = IStatus.none
    ok_project: IStatus = IStatus.none  
    ok_user: IStatus = IStatus.none
    ok_all: IStatus = IStatus.none    

    class Config:
        orm_mode = True

#crud

class ProjectStateInitSchema(ProjectStateBaseSchema):
    ...

class ProjectStateCreateSchema(ProjectStateInitSchema):
    ...

class ProjectStateUpdateSchema(ProjectStateInitSchema):
    ...

class ProjectStateProcessSchema(BaseSchema):
    project_id: int
    active: IStatus = IStatus.none
    billing: IStatus = IStatus.none
    ohs: IStatus = IStatus.none
    rdm: IStatus = IStatus.none
    phase: IStatus = IStatus.none
    ok_project: IStatus = IStatus.none      

    class Config:
        orm_mode = True

class ProjectStatePostProcessUpdateSchema(BaseSchema):
    project_id: int
    ok_project: IStatus = IStatus.none
    ok_user: IStatus = IStatus.none
    ok_all: IStatus = IStatus.none

    class Config:
        orm_mode = True

#presentation

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