from typing import Optional

from pydantic import BaseModel

class SystemBaseSchema(BaseModel):
    id: int
    type: str
    name: str
    class Config:
        orm_mode = True

# Properties on creation
class SystemCreateSchema(SystemBaseSchema):
    ...

# Properties on update
class SystemUpdateSchema(SystemBaseSchema):
    ...