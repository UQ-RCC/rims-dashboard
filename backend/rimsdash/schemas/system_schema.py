from typing import Optional, ForwardRef

from .base_schema import BaseSchema

SystemUserOutSchema = ForwardRef('SystemUserOutSchema')
SystemUserOutRefsFromSystemSchema = ForwardRef('SystemUserOutRefsFromSystemSchema')

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
class SystemOutSchema(SystemBaseSchema):
    """
    No references, terminates recursion
    """ 
    ...

#export schema
class SystemOutInfoSchema(SystemBaseSchema):
    """
    No references, terminates recursion
    """ 
    ...
    system_rights: Optional[list[SystemUserOutSchema]]

#export schema
class SystemOutRefsSchema(SystemBaseSchema):
    """
    No references, terminates recursion
    """ 
    ...
    system_rights: Optional[list[SystemUserOutRefsFromSystemSchema]]



from .systemuser_schema import SystemUserOutSchema, SystemUserOutRefsFromSystemSchema

SystemOutInfoSchema.update_forward_refs()
SystemOutRefsSchema.update_forward_refs()
