from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Enum, DateTime, Date, Time, Interval, ForeignKeyConstraint, null
from sqlalchemy.orm import relationship

from rimsdash.db import Base

class SystemModel(Base):
    #__tablename__ = 'system'
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, primary_key=False, index=False, nullable=False)
    name = Column(String, primary_key=False, index=False, nullable=False)
