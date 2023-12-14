from typing import Optional, ForwardRef

from .base_schema import BaseSchema

from rimsdash.models import IStatus


UserOutSchema=ForwardRef('UserOutSchema')

class UserStateBaseSchema(BaseSchema):
    username: str
    ok: IStatus = IStatus.disabled
    active: IStatus = IStatus.disabled
    access_aibn: IStatus = IStatus.off
    access_hawken: IStatus = IStatus.off
    access_chem: IStatus = IStatus.off
    access_qbp: IStatus = IStatus.off
    access_pitschi: IStatus = IStatus.disabled 
    ok_project: IStatus = IStatus.disabled

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



class UserStatePostProcessUpdateSchema(BaseSchema):
    username: str
    ok_project: IStatus = IStatus.disabled

    class Config:
        orm_mode = True


from .user_schema import UserOutSchema

UserStateOutInfoSchema.update_forward_refs()