from enum import Enum
from pydantic import BaseModel

class BaseSchema(BaseModel):
    """
    extension of BaseModel with simple helper methods
    """
    ...

    def to_dict(self, literal: bool = False) -> dict:
        """
        return as dictionary
        """
        result = {}
        for key in self.__dict__:
            __value = getattr(self, key)

            if literal and isinstance(__value, Enum):
                __value = __value.value

            result[key] = __value
        return result