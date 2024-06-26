from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, Float, Enum, DateTime, Date, Time, Interval, ForeignKeyConstraint, null
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship

from .base_model import Base, AdminRight
#from .systemuser_models import SystemUserModel

class UserModel(Base):
    __tablename__ = 'rduser'
    username = Column(String, primary_key=True, index=True)
    name = Column(String, primary_key=False, index=False, nullable=False)
    userid = Column(Integer, primary_key=False, index=False, nullable=False)
    email = Column(String, primary_key=False, index=False, nullable=False)
    group = Column(String, primary_key=False, index=False, nullable=False)
    active = Column(Boolean, primary_key=False, index=False, nullable=False, default=False)
#    admin = Column(Boolean, primary_key=False, index=False, nullable=True)
    admin = Column(Enum(AdminRight), primary_key=False, index=False, nullable=True)
    #rights = Column(MutableDict.as_mutable(JSON), primary_key=False, index=False, nullable=True, default={})
    #   strings to avoid circular import - ie. SystemUserModel.user    
    system_rights = relationship('SystemUserModel', back_populates='user')
    project_rights = relationship("ProjectUsersModel", back_populates="user")
    training_requests = relationship("TrainingRequestModel", back_populates="user")
    user_state = relationship("UserStateModel", back_populates="user", uselist=False)
  

    def to_dict(self, literal: bool = False) -> dict:

        """
        deprecated, use Pydantic schema .json() instead
        """

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