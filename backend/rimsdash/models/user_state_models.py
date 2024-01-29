from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Enum, DateTime, Date, Time, Interval, ForeignKeyConstraint, null
from sqlalchemy.orm import relationship

from .base_model import Base, IStatus


class UserStateModel(Base):
    __tablename__ = 'rduserstate'
    username = Column(String, ForeignKey('rduser.username'), primary_key=True, index=True)    
    ok = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.none)
    active = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.none)
    access_aibn = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.none)
    access_hawken = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.none)
    access_chem = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.none)
    access_qbp = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.none)
    access_pitschi = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.none) 
    ok_project =  Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.none)
    user = relationship("UserModel", back_populates="user_state")