from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Enum, DateTime, Date, Time, Interval, ForeignKeyConstraint, null
from sqlalchemy.orm import relationship

from .base_model import Base

class ProjectModel(Base):
    __tablename__ = 'rdproject'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, primary_key=False, index=False, nullable=False)    
    phase = Column(Integer, primary_key=False, index=False, nullable=False)
    active = Column(Boolean, primary_key=False, index=False, nullable=False, default=False)    
    type = Column(String, primary_key=False, index=False, nullable=False) 
    group = Column(String, primary_key=False, index=False, nullable=False) 
    coreid = Column(Integer, primary_key=False, index=False, nullable=False, default=2)
    bcode = Column(String, primary_key=False, index=False, nullable=True) 
    affiliation = Column(String, primary_key=False, index=False, nullable=True)    
    description = Column(String, primary_key=False, index=False, nullable=True)
    qcollection = Column(String, primary_key=False, index=False, nullable=True)
    status = Column(String, primary_key=False, index=False, nullable=True)

    #users = relationship("UserProject", back_populates="project")