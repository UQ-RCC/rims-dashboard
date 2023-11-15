from typing import Optional

from .base_schema import BaseSchema

from rimsdash.models import IStatus

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

class UserStateTerminalSchema(UserStateBaseSchema):
    """
    No onward references, terminates recursion
    """    
    ...