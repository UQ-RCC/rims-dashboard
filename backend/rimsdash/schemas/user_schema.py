from typing import Optional

from .base_schema import BaseSchema

from .userproject_schema import UserProjectBaseSchema

class UserBaseSchema(BaseSchema):
    username: str
    name: str
    userid: Optional[int]
    email: str
    group: str
    active: bool
    class Config:
        orm_mode = True

# Properties on creation
class UserCreateSchema(UserBaseSchema):
    userid: int
    ...

# Properties on update
class UserUpdateSchema(UserBaseSchema):
    ...

class UserReceiveSchema(UserBaseSchema):
    ...


class UserFullSchema(UserBaseSchema):
    username: str
    name: str
    userid: Optional[int]
    email: str
    group: str
    active: bool
    projects: Optional[list[UserProjectBaseSchema]] = []