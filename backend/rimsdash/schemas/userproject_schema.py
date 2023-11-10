from typing import Optional

from .base_schema import BaseSchema
#from .user_schema import UserFullSchema
#from .project_schema import ProjectFullSchema

class UserProjectBaseSchema(BaseSchema):
    username: str
    projectid: int
"""
class UserProjectFullSchema(UserProjectBaseSchema):
    user: UserFullSchema
    project: ProjectFullSchema
    bookings: List[Booking] = []
    datasets: List[Dataset] = [] 
    class Config:
        orm_mode = True
"""

