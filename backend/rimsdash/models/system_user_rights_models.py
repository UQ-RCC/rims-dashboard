from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, Float, Enum, DateTime, Date, Time, Interval, ForeignKeyConstraint, null
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship

from .base_model import Base, AccessLevel
from .user_models import UserModel
from .system_models import SystemModel

class SystemUserRightsModel(Base):
    """
    junction table linking user + system with rights level
    """
    __tablename__ = 'rdsystemrights'
    username = Column(String, ForeignKey('rduser.username'), primary_key=True)      #maybe use a direct reference here eg. User.username
    system_id = Column(Integer, ForeignKey('rdsystem.id'), primary_key=True)
    access_level = Column(Enum(AccessLevel), primary_key=False, index=False, nullable=False)
    #user = relationship(UserModel, back_populates=UserModel.system_rights)
    #system = relationship(SystemModel, back_populates=SystemModel.user_rights)


"""
to use:
    junction = session.query(JunctionTable).filter_by(table1_id=table1_id, table2_id=table2_id).first()

    if junction.status == 'OK':
        print('yes')
"""