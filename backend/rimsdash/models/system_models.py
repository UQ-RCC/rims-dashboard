from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Enum, DateTime, Date, Time, Interval, ForeignKeyConstraint, null
from sqlalchemy.orm import relationship

from .base_model import Base
#from .system_user_rights_models import SystemUserRightsModel

class SystemModel(Base):
    __tablename__ = 'rdsystem'
    id = Column(Integer, primary_key=True, index=True)
    system_type = Column(String, primary_key=False, index=False, nullable=False)
    name = Column(String, primary_key=False, index=False, nullable=False)
    #   strings to avoid circular import - ie. SystemUserRightsModel.system        
    user_rights = relationship('SystemUserRightsModel', back_populates='system')
