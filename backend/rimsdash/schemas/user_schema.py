from typing import Optional, TypedDict, Dict

from rimsdash.models import AccessLevel

from .base_schema import BaseSchema

from .userproject_schema import UserProjectBaseSchema

AccessDict = Dict[int, AccessLevel]

class UserBaseSchema(BaseSchema):
    username: str
    name: str
    userid: Optional[int]
    email: str
    group: str
    active: bool

    class Config:
        orm_mode = True

#complete DB schema with all fields
class UserFullSchema(UserBaseSchema):
    username: str
    name: str
    userid: Optional[int]
    email: str
    group: str
    active: bool
    admin: bool = False
    #rights: Optional[AccessDict] = {}
    projects: Optional[list[UserProjectBaseSchema]] = []

# Properties on creation
class UserCreateSchema(UserBaseSchema):
    userid: int
    ...

# Properties on update
class UserUpdateSchema(UserBaseSchema):
    ...

class UserReceiveSchema(UserBaseSchema):
    ...

# Access rights only
class UserCreateRightsSchema(BaseSchema):
    username: str
    rights: Optional[AccessDict] = {}

    class Config:
        orm_mode = True