from typing import Optional, ForwardRef

from .base_schema import BaseSchema

from rimsdash.models import IStatus


UserOutSchema=ForwardRef('UserOutSchema')
UserOutInfoSchema=ForwardRef('UserOutInfoSchema')

class UserStateBaseSchema(BaseSchema):
    username: str
    ok: IStatus = IStatus.off
    active: IStatus = IStatus.off
    access_aibn: IStatus = IStatus.off
    access_hawken: IStatus = IStatus.off
    access_chem: IStatus = IStatus.off
    access_qbp: IStatus = IStatus.off

    class Config:
        orm_mode = True

class UserStateCreateSchema(UserStateBaseSchema):
    ...

class UserStateUpdateSchema(UserStateBaseSchema):
    ...




class UserStateOutSchema(UserStateBaseSchema):
    """
    No onward references, terminates recursion
    """
    ...

class UserStateOutInfoSchema(UserStateBaseSchema):
    """
    No onward references, terminates recursion
    """
    user: UserOutSchema


class ProjectStateExportFullRefsSchema(UserStateBaseSchema):
    """
    No onward references, terminates recursion
    """
    user: UserOutInfoSchema



from .user_schema import UserOutSchema, UserOutInfoSchema

UserStateOutInfoSchema.update_forward_refs()
ProjectStateExportFullRefsSchema.update_forward_refs()