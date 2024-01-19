from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Enum, DateTime, Date, Time, Interval, ForeignKeyConstraint, null
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from .base_model import Base, IStatus

class TrainingRequestModel(Base):
    __tablename__ = 'rdtrainingrequests'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=True)
    new = Column(Boolean, primary_key=False, index=False, nullable=False)
    type = Column(String, primary_key=False, index=False, nullable=True)
    form_id = Column(Integer, primary_key=False, index=False, nullable=False)
    form_name = Column(String, primary_key=False, index=False, nullable=False)
    username = Column(String, ForeignKey('rduser.username'), primary_key=False)
    form_data = Column(JSONB, primary_key=False, index=False, nullable=True)
    state = Column(Enum(IStatus), primary_key=False, index=False, nullable=False, default=IStatus.off)
    user = relationship("UserModel", back_populates="training_requests")