from enum import Enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Enum, DateTime, Date, Time, Interval, ForeignKeyConstraint, null
from datetime import datetime

from .base_model import Base, SyncType



class SyncModel(Base):
    __tablename__ = 'rdsync'
    id = Column(Integer, primary_key=True, index=True)
    sync_type = Column(Enum(SyncType), nullable=False, default=SyncType.none) 
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)    
    complete = Column(Boolean, default=False)