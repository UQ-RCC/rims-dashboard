from datetime import datetime
from pydantic import Field

from typing import Optional, ForwardRef

from .base_schema import BaseSchema

UserOutSchema = ForwardRef('UserOutSchema')

class TrainingRequestBaseSchema(BaseSchema):
    id: int
    date: datetime
    new: bool
    type: str
    form_id: int
    form_name: str
    username: str
    #NB: username in DB but uid from external API, must be converted on ingest

    class Config:
        orm_mode = True

# Properties on update
class TrainingRequestReceiveSchema(BaseSchema):
    id: int
    date: datetime
    new: bool
    type: str
    form_id: int
    form_name: str
    user_id: int
    #NB: uid NOT in DB, ingested from rims and converted in services  

    class Config:
        orm_mode = True


class TrainingRequestReceiveFormDataSchema(BaseSchema):
    id: int
    date: datetime
    user_fullname: str
    #NB: user_fullname NOT in DB, ingested from rims and converted in services
    form_data: Optional[dict] = Field(None, example={'key': 'value'})
    #NB: area NOT in DB, test for report #78
    
    class Config:
        orm_mode = True


# Properties on update
class TrainingRequestCreateSchema(TrainingRequestBaseSchema):
    ...

class TrainingRequestUpdateSchema(TrainingRequestBaseSchema):
    ...

class TrainingRequestAddFormDataSchema(BaseSchema):
    id: int
    form_data: Optional[dict] = Field(None, example={'key': 'value'})

    class Config:
        orm_mode = True

#export schema
#---------------
#   naming convention:  
#       out > info > refs > extended > full

class TrainingRequestOutSchema(TrainingRequestBaseSchema):
    """
    No references, terminates recursion
    """ 
    ...

class TrainingRequestOutInfoSchema(TrainingRequestBaseSchema):
    """
    No references, terminates recursion
    """ 
    ...
    user: Optional[UserOutSchema]


from .user_schema import UserOutSchema

UserOutSchema.update_forward_refs()
