import typing
from enum import Enum

from sqlalchemy.ext.declarative import as_declarative

class_registry: typing.Dict = {}

@as_declarative(class_registry=class_registry)
class Base:
    """
    Base class for database

    Version of declarative_base() allowing simple extension
    """

    ...
    #id: typing.Any
    #__name__: str

    def to_dict(self, literal: bool = False) -> dict:
        """
        return as dictionary
        """
        result = {}
        for column in self.__table__.columns:
                __value = getattr(self, column.name)

                if literal and isinstance(__value, Enum):
                    __value = __value.value

                result[column.name] = __value
        return result

    """
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    """


class IStatus(Enum):
    """
    enum for indicator state values
    """    
    #in progress------- 
    off = 'off'
    incomplete = 'incomplete'
    waiting = 'waiting'
    ready = 'ready'
    extended = 'extended'
    disabled = 'disabled'
    #error------------
    warn = 'warn'
    fail = 'fail'
    na = 'na'

class AccessLevel(Enum):
    """
    enum for RIMS used rights
    """    
    deactivated = 'D'
    novice = 'N'
    autonomous = 'A'
    superuser = 'S'