from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, Float, Enum, DateTime, Date, Time, Interval, ForeignKeyConstraint, null
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship

from .base_model import Base, AccessLevel

class SystemRightsModel(Base):
    """
    junction table linking user + system with rights level
    """
    __tablename__ = 'rdsystemrights'
    username = Column(String, ForeignKey('rduser.username'), primary_key=True)
    system_id = Column(Integer, ForeignKey('rdsystem.id'), primary_key=True)
    status = Column(AccessLevel, primary_key=False, index=False, nullable=False)