from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, Float, Enum, DateTime, Date, Time, Interval, ForeignKeyConstraint, null
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship

from .base_model import Base

class UserModel(Base):
    __tablename__ = 'rduser'
    username = Column(String, primary_key=True, index=True)
    name = Column(String, primary_key=False, index=False, nullable=False)
    userid = Column(Integer, primary_key=False, index=False, nullable=False)
    email = Column(String, primary_key=False, index=False, nullable=False)
    group = Column(String, primary_key=False, index=False, nullable=False)
    active = Column(Boolean, primary_key=False, index=False, nullable=False, default=False)
    admin = Column(Boolean, primary_key=False, index=False, nullable=True, default=False)
    rights = Column(MutableDict.as_mutable(JSON), primary_key=False, index=False, nullable=True, default={})

    #projects = relationship("UserProject", back_populates="user")  