from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Enum, DateTime, Date, Time, Interval, ForeignKeyConstraint, null
from sqlalchemy.orm import relationship

from .base_model import Base, IStatus


class UserStateModel(Base):
    __tablename__ = 'rduserstate'
    username = Column(String, ForeignKey('rduser.username'), primary_key=True)    
    ok = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.off)
    active = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.off)
    access_aibn = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.off)
    access_hawken = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.off)
    access_chem = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.off)
    access_qbp = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.off)
    access_pitschi = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.off) 
    ok_project =  Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.off)
    user = relationship("UserModel", back_populates="user_state")