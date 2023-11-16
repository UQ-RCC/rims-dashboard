from typing import Optional, ForwardRef

from .base_schema import BaseSchema

SystemUserOutSchema = ForwardRef('SystemUserOutSchema')

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


#export schema
#---------------
#   naming convention:  
#       out > info > refs > extended > full

class SystemOutSchema(SystemBaseSchema):
    """
    No references, terminates recursion
    """ 
    ...

class SystemOutInfoSchema(SystemBaseSchema):
    """
    No references, terminates recursion
    """ 
    ...
    system_rights: Optional[list[SystemUserOutSchema]]



from .systemuser_schema import SystemUserOutSchema

SystemOutInfoSchema.update_forward_refs()
