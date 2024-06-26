from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, Float, Enum, DateTime, Date, Time, Interval, ForeignKeyConstraint, null
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship

from .base_model import Base, SystemRight
from .user_models import UserModel
from .system_models import SystemModel

class SystemUserModel(Base):
    """
    junction table linking user + system with rights level
    """
    __tablename__ = 'rdsystemrights'
    username = Column(String, ForeignKey('rduser.username'), primary_key=True)      #maybe use a direct reference here eg. User.username
    system_id = Column(Integer, ForeignKey('rdsystem.id'), primary_key=True)
    status = Column(Enum(SystemRight), primary_key=False, index=False, nullable=False)
    #   strings to avoid circular import - ie. UserModel.system_rights
    user = relationship("UserModel", back_populates="system_rights")
    system = relationship("SystemModel", back_populates="user_rights")



"""
to use:
    junction = session.query(JunctionTable).filter_by(table1_id=table1_id, table2_id=table2_id).first()

    if junction.status == 'OK':
        print('yes')
"""