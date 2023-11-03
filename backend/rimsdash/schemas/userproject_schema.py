from typing import Optional

from pydantic import BaseModel

class UserProjectBaseSchema(BaseModel):
    username: str
    projectid: int

