from typing import Optional, ForwardRef

from .base_schema import BaseSchema

from rimsdash.models import IStatus


UserOutSchema=ForwardRef('UserOutSchema')

class UserStateBaseSchema(BaseSchema):
    username: str
    ok: IStatus = IStatus.none
    active: IStatus = IStatus.none
    access_aibn: IStatus = IStatus.none
    access_hawken: IStatus = IStatus.none
    access_chem: IStatus = IStatus.none
    access_qbp: IStatus = IStatus.none
    access_pitschi: IStatus = IStatus.none 
    ok_project: IStatus = IStatus.none

    class Config:
        orm_mode = True

class UserStateCreateSchema(UserStateBaseSchema):
    ...

class UserStateUpdateSchema(UserStateBaseSchema):
    ...


class UserStateReceiveSchema(UserStateBaseSchema):
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
    ok_project: IStatus = IStatus.none

    class Config:
        orm_mode = True


from .user_schema import UserOutSchema

UserStateOutInfoSchema.update_forward_refs()