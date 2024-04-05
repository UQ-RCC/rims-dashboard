from typing import Optional, ForwardRef

from .base_schema import BaseSchema

from rimsdash.models import IStatus


UserOutSchema=ForwardRef('UserOutSchema')

class UserStateBaseSchema(BaseSchema):
    username: str
    active: IStatus = IStatus.none
    access_aibn: IStatus = IStatus.none
    access_hawken: IStatus = IStatus.none
    access_chem: IStatus = IStatus.none
    access_qbp: IStatus = IStatus.none
    access_pitschi: IStatus = IStatus.none 
    ok_user: IStatus = IStatus.none
    ok_project: IStatus = IStatus.none
    ok_all: IStatus = IStatus.none

    class Config:
        orm_mode = True

#crud
        
class UserStateInitSchema(UserStateBaseSchema):
    ...

class UserStateCreateSchema(UserStateInitSchema):
    ...

class UserStateUpdateSchema(UserStateInitSchema):
    ...

class UserStateProcessSchema(BaseSchema):
    username: str
    active: IStatus = IStatus.none
    access_aibn: IStatus = IStatus.none
    access_hawken: IStatus = IStatus.none
    access_chem: IStatus = IStatus.none
    access_qbp: IStatus = IStatus.none
    access_pitschi: IStatus = IStatus.none
    ok_user: IStatus = IStatus.none  

    class Config:
        orm_mode = True    

class UserStatePostProcessUpdateSchema(BaseSchema):
    username: str
    ok_user: IStatus = IStatus.none
    ok_project: IStatus = IStatus.none
    ok_all: IStatus = IStatus.none

    class Config:
        orm_mode = True


#presentation

class UserStateOutSchema(UserStateBaseSchema):
    """
    No onward references, terminates recursion
    """
    ...

class UserStateOutInfoSchema(UserStateBaseSchema):
    """
    includes user details
    """
    user: UserOutSchema



from .user_schema import UserOutSchema

UserStateOutInfoSchema.update_forward_refs()