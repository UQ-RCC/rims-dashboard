from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Enum, DateTime, Date, Time, Interval, ForeignKeyConstraint, null
from sqlalchemy.orm import relationship

from rimsdash.db.base_class import Base

class UserModel(Base):
    __tablename__ = 'rduser'
    username = Column(String, primary_key=True, index=True)
    name = Column(String, primary_key=False, index=False, nullable=False)
    userid = Column(Integer, primary_key=False, index=False, nullable=True)
    email = Column(String, primary_key=False, index=False, nullable=False)
    group = Column(String, primary_key=False, index=False, nullable=True)
    active = Column(Boolean, primary_key=False, index=False, nullable=False, default=False)
    #projects = relationship("UserProject", back_populates="user")  