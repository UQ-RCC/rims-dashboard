from enum import Enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Enum, DateTime, Date, Time, Interval, ForeignKeyConstraint, null
from datetime import datetime

from .base_model import Base


class SyncType(Enum):
    minor = 'minor'
    full = 'full'
    report_only = 'report_only' 

class SyncModel(Base):
    __tablename__ = 'rdsync'
    id = Column(Integer, primary_key=True, index=True)
    sync_type = Column(Enum(SyncType), nullable=True) 
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)    
    complete = Column(Boolean, default=False)