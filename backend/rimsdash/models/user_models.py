from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, Float, Enum, DateTime, Date, Time, Interval, ForeignKeyConstraint, null
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship

from .base_model import Base
#from .system_user_rights_models import SystemUserRightsModel

class UserModel(Base):
    __tablename__ = 'rduser'
    username = Column(String, primary_key=True, index=True)
    name = Column(String, primary_key=False, index=False, nullable=False)
    userid = Column(Integer, primary_key=False, index=False, nullable=False)
    email = Column(String, primary_key=False, index=False, nullable=False)
    group = Column(String, primary_key=False, index=False, nullable=False)
    active = Column(Boolean, primary_key=False, index=False, nullable=False, default=False)
    admin = Column(Boolean, primary_key=False, index=False, nullable=True, default=False)
    #rights = Column(MutableDict.as_mutable(JSON), primary_key=False, index=False, nullable=True, default={})
    #   strings to avoid circular import - ie. SystemUserRightsModel.user    
    system_rights = relationship('SystemUserRightsModel', back_populates='user')
    projects = relationship("ProjectUsersModel", back_populates="user")  

    def to_dict(self, literal: bool = False) -> dict:

        result = {}
        for column in self.__table__.columns:
                __value = getattr(self, column.name)

                if literal and isinstance(__value, Enum):
                    __value = __value.value

                result[column.name] = __value

        rights_list = getattr(self, "system_rights")

        if not literal:
            result["system_rights"] = rights_list
        else:
            rights_dict = {}
            for right in rights_list:
                rights_dict[right.system_id] = right.status.value

            result["system_rights"] = rights_dict

        return result