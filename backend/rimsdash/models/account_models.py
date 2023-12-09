from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Enum, DateTime, Date, Time, Interval, ForeignKeyConstraint, null
from sqlalchemy.orm import relationship

from .base_model import Base
#from .systemuser_models import SystemUserModel

class AccountModel(Base):
    __tablename__ = 'rdaccount'
    bcode = Column(String, primary_key=True, index=False, nullable=False)
    account_projects = relationship('ProjectAccountModel', back_populates='account')