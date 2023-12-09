from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, Float, Enum, DateTime, Date, Time, Interval, ForeignKeyConstraint, null
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship

from .base_model import Base

class ProjectAccountModel(Base):
    """
    junction table linking project + account with validity
    """
    __tablename__ = 'rdprojectaccount'
    bcode = Column(String, ForeignKey('rdaccount.bcode'), primary_key=True)      #maybe use a direct reference here eg. User.username
    project_id = Column(Integer, ForeignKey('rdproject.id'), primary_key=True)
    valid = Column(Boolean, primary_key=False, index=False, nullable=False)
    account = relationship("AccountModel", back_populates="account_projects")
    project = relationship("ProjectModel", back_populates="project_account")