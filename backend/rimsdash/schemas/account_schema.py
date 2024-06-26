from .base_schema import BaseSchema

class AccountBaseSchema(BaseSchema):
    bcode: str

    class Config:
        orm_mode = True

# Properties on creation
class AccountReceiveSchema(AccountBaseSchema):
    ...

# Properties on update
class AccountUpdateSchema(AccountBaseSchema):
    ...

class AccountCreateSchema(AccountBaseSchema):
    ...


#export schema
#---------------
#   naming convention:  
#       out > info > refs > extended > full

class AccountOutSchema(AccountBaseSchema):
    ...