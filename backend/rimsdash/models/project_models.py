from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Enum, DateTime, Date, Time, Interval, ForeignKeyConstraint, null
from sqlalchemy.orm import relationship

from rimsdash.db.base_class import Base

class ProjectModel(Base):
    __tablename__ = 'rdproject'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, primary_key=False, index=False, nullable=False)
    type = Column(String, primary_key=False, index=False, nullable=False) 
    phase = Column(Integer, primary_key=False, index=False, nullable=False)
    description = Column(String, primary_key=False, index=False, nullable=True)
    qcollection = Column(String, primary_key=False, index=False, nullable=True)
    coreid = Column(Integer, primary_key=False, index=False, nullable=False, default=2)
    bcode = Column(String, primary_key=False, index=False, nullable=True) 
    active = Column(Boolean, primary_key=False, index=False, nullable=False, default=False)    
    #users = relationship("UserProject", back_populates="project")