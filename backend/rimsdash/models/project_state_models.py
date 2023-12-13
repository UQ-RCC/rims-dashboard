from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Enum, DateTime, Date, Time, Interval, ForeignKeyConstraint, null
from sqlalchemy.orm import relationship

from .base_model import Base, IStatus


class ProjectStateModel(Base):
    __tablename__ = 'rdprojectstate'
    project_id = Column(Integer, ForeignKey('rdproject.id'), primary_key=True)    
    ok = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.off)
    active = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.off)
    billing = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.off)
    ohs = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.off)
    rdm = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.off)
    phase = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.off)
    ok_user =  Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.off)
    project = relationship("ProjectModel", back_populates="project_state") 
