from pydantic import BaseModel

class BaseSchema(BaseModel):
    """
    extension of BaseModel with simple helper methods
    """
    ...

    def to_dict(self):
        return self.__dict__