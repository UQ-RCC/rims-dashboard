from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Enum, DateTime, Date, Time, Interval, ForeignKeyConstraint, null

from .base_model import Base, IStatus


class UserStateModel(Base):
    __tablename__ = 'rduserstate'
    overall = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.off)
    active = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.off)
    access_aibn = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.off)
    access_hawken = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.off)
    access_chem = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.off)
    access_qbp = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.off)