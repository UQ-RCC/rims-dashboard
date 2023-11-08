from typing import Optional

from .base_schema import BaseSchema

class SystemBaseSchema(BaseSchema):
    id: int
    system_type: str
    name: str
    class Config:
        orm_mode = True

# Properties on creation
class SystemCreateSchema(SystemBaseSchema):
    ...

# Properties on update
class SystemUpdateSchema(SystemBaseSchema):
    ...

# Properties on update
class SystemReceiveSchema(SystemBaseSchema):
    ...