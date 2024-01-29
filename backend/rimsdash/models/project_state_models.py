from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Enum, DateTime, Date, Time, Interval, ForeignKeyConstraint, null
from sqlalchemy.orm import relationship

from .base_model import Base, IStatus


class ProjectStateModel(Base):
    __tablename__ = 'rdprojectstate'
    project_id = Column(Integer, ForeignKey('rdproject.id'), primary_key=True, index=True)    
    ok = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.none)
    active = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.none)
    billing = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.none)
    ohs = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.none)
    rdm = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.none)
    phase = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.none)
    ok_user =  Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.none)
    project = relationship("ProjectModel", back_populates="project_state") 
