from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Enum, DateTime, Date, Time, Interval, ForeignKeyConstraint, null

from .base_model import Base, IStatus


class ProjectStateModel(Base):
    __tablename__ = 'rdprojectstate'
    id = Column(Integer, primary_key=True, index=True)    
    ok = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.off)
    active = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.off)
    billing = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.off)
    ohs = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.off)
    rdm = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.off)
    phase = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.off)
