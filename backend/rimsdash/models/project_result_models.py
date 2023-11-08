from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Enum, DateTime, Date, Time, Interval, ForeignKeyConstraint, null
from sqlalchemy.orm import relationship

from rimsdash.db.base_class import Base

class ProjectModel(Base):
    #__tablename__ = 'project'
    id = Column(Integer, primary_key=True, index=True)
    #users = relationship("UserProject", back_populates="project")