from typing import Optional

from pydantic import BaseModel

from .userproject_schema import UserProjectBaseSchema

class UserBaseSchema(BaseModel):
    username: str
    name: str
    #userid: Optional[int] = None
    userid: int | None     #optional
    email: str
    group: str
    active: bool
    projects: list[UserProjectBaseSchema] = []
    class Config:
        orm_mode = True

# Properties on creation
class UserCreateSchema(UserBaseSchema):
    userid: int

# Properties on update
class UserUpdateSchema(UserBaseSchema):
    ...