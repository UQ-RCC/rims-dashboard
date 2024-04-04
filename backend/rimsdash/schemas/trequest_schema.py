from datetime import datetime
from pydantic import Field, root_validator
from typing import Optional, ForwardRef

import rimsdash.config as config

from rimsdash.models import IStatus

from .base_schema import BaseSchema


RIMS_URL = config.get('ppms', 'rims_url', required=True)
CORE_ID = config.get('ppms', 'core_id', required=True)

UserOutSchema = ForwardRef('UserOutSchema')
UserOutWithStateSchema = ForwardRef('UserOutWithStateSchema')

class TrainingRequestBaseSchema(BaseSchema):
    id: int
    date: datetime
    new: bool
    type: str
    form_id: int
    form_name: str
    username: str
    state: IStatus = IStatus.none    
    #NB: username in DB but uid from external API, must be converted on ingest

    class Config:
        orm_mode = True

# Properties from external API
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

# Form properties from external API
class TrainingRequestReceiveFormDataSchema(BaseSchema):
    id: int
    date: datetime
    user_fullname: str
    #NB: user_fullname NOT in DB, ingested from rims and converted in services
    form_data: Optional[dict] = Field(None, example={'key': 'value'})
    
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

class TrainingRequestUpdateStateSchema(BaseSchema):
    id: int
    state: IStatus = IStatus.none

    class Config:
        orm_mode = True


#processing schema
#---------------
class TrainingRequestForProcessingSchema(TrainingRequestBaseSchema):
    """
    No references, terminates recursion
    """ 
    ...
    user: Optional[UserOutWithStateSchema]


#export schema
#---------------
#   naming convention:  
#       out > info > refs > extended > full

class TrainingRequestOutSchema(TrainingRequestBaseSchema):
    """
    No references, terminates recursion
    """ 
    ...
    form_data: Optional[dict] = Field(None, example={'key': 'value'})
    #use root_validator to add a computed property that will return via .dict() & .json()
    #   if not needed via json, use @property instead
    @root_validator
    def add_url(cls, values) -> str:
        if isinstance(values, dict) and 'id' in values:
            values['url'] = f'{RIMS_URL}/proctrain/?pf={CORE_ID}&trainreq={values.get("id")}'
        return values
        #   NB: operate via values dict rather than on self directly


class TrainingRequestOutWithFormSchema(TrainingRequestOutSchema):
    ...
    #form_data: Optional[dict] = Field(default_factory=dict, example={'key': 'value'})

class TrainingRequestOutWithUserSchema(TrainingRequestOutWithFormSchema):
    """
    No references, terminates recursion
    """ 
    ...
    user: Optional[UserOutSchema]

class TrainingRequestOutWithUserStateSchema(TrainingRequestOutSchema):
    """
    No references, terminates recursion
    """ 
    ...
    user: Optional[UserOutWithStateSchema]


from .user_schema import UserOutWithStateSchema
from .user_schema import UserOutSchema


TrainingRequestForProcessingSchema.update_forward_refs()
TrainingRequestOutWithUserSchema.update_forward_refs()
TrainingRequestOutWithUserStateSchema.update_forward_refs()

