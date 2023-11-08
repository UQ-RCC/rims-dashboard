from typing import Optional

from .base_schema import BaseSchema

class UserProjectBaseSchema(BaseSchema):
    username: str
    projectid: int

