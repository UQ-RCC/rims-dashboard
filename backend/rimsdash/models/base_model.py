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
    none = '0_none'
    incomplete = '1_incomplete'
    warn = '2_warn'
    off = '3_off'
    ready = '4_ready'
    extended = '5_extended'

    #in progress------- 
    #off = 'off'
    #incomplete = 'incomplete'
    #waiting = 'waiting'
    #ready = 'ready'
    #extended = 'extended'
    #disabled = 'disabled'
    #error------------
    #warn = 'warn'
    #fail = 'fail'
    #na = 'na'
    #none = 'none'

class SystemRight(Enum):
    """
    enum for RIMS used rights
    """    
    deactivated = 'D'
    novice = 'N'
    autonomous = 'A'
    superuser = 'S'


class ProjectRight(Enum):
    """
    enum for RIMS used rights
    """    
    member = 'M'
    owner = 'PO'
    admin = 'PA'

class AdminRight(Enum):
    """
    enum for RIMS used rights
    """    
    none = 'None'  
    user = 'User'
    previous = 'PreviousAdmin'
    admin = 'Admin'
 

class SyncType(Enum):
    """
    enum for sync types
    """
    none = 'none'
    individual = 'individual'
    update = 'update'
    full = 'full'
    rebuild = 'rebuild'

class SyncStatus(Enum):
    """
    enum for sync types
    """
    none = 'none'
    in_progress = 'in_progress'
    complete = 'complete'
    failed = 'failed'