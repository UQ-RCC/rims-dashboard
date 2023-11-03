from typing import Optional

from pydantic import BaseModel

"""
DEPRECATING
"""

###################################################
############### RIMS data #########################

class UserProjectBase(BaseModel):
    username: str
    projectid: int

class System(BaseModel):
    id: int
    type: str
    name: str
    class Config:
        orm_mode = True

class User(BaseModel):
    username: str
    name: str
    #userid: Optional[int] = None
    userid: int | None     #optional
    email: str
    group: str
    active: bool
    projects: list[UserProjectBase] = []
    class Config:
        orm_mode = True

class Project(BaseModel):
    id: int
    title: str
    type: str
    phase: int
    description: Optional[str] = None
    qcollection: Optional[str] = None
    coreid: int = 2
    #bcode = Optional[str] = None
    users: list[UserProjectBase] = []
    active: bool = False
    class Config:
        orm_mode = True

class UserProject(UserProjectBase):
    user: User
    project: Project
    class Config:
        orm_mode = True