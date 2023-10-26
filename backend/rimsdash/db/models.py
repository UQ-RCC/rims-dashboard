import enum, datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Enum, DateTime, Date, Time, Interval, ForeignKeyConstraint, null
from sqlalchemy.orm import relationship

from sqlalchemy.ext.mutable import MutableList
from sqlalchemy_json import mutable_json_type
from sqlalchemy import PickleType
import pytz
import rimsdash.config as config
from sqlalchemy.dialects.postgresql import JSONB


from .database import Base


class System(Base):
    __tablename__ = 'system'
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, primary_key=False, index=False, nullable=False)
    name = Column(String, primary_key=False, index=False, nullable=False)

class UserProject(Base):
    __tablename__ = 'userproject'
    username = Column(String, ForeignKey('user.username'), primary_key=True)
    projectid = Column(Integer, ForeignKey('project.id'), primary_key=True)
    project = relationship("Project", back_populates="users")
    user = relationship("User", back_populates="projects")
    
class User(Base):
    __tablename__ = 'user'
    username = Column(String, primary_key=True, index=True)
    name = Column(String, primary_key=False, index=False, nullable=False)
    userid = Column(Integer, primary_key=False, index=False, nullable=True)
    email = Column(String, primary_key=False, index=False, nullable=False)
    group = Column(String, primary_key=False, index=False, nullable=True)
    active = Column(Boolean, primary_key=False, index=False, nullable=False, default=False)
    projects = relationship("UserProject", back_populates="user")    

class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, primary_key=False, index=False, nullable=False)
    type = Column(String, primary_key=False, index=False, nullable=False) 
    phase = Column(Integer, primary_key=False, index=False, nullable=False)
    description = Column(String, primary_key=False, index=False, nullable=True)
    qcollection = Column(String, primary_key=False, index=False, nullable=True)
    coreid = Column(Integer, primary_key=False, index=False, nullable=False, default=2)
    bcode = Column(String, primary_key=False, index=False, nullable=True) 
    active = Column(Boolean, primary_key=False, index=False, nullable=False, default=False)    
    users = relationship("UserProject", back_populates="project")
