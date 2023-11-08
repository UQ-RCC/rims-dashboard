import typing
import enum

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

    def to_dict(self) -> dict:
        """
        return as dictionary
        """
        result = {}
        for column in self.__table__.columns:
                __value = getattr(self, column.name)

                if isinstance(__value, enum.Enum):
                    __value = __value.value

                result[column.name] = __value
        return result

    """
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    """