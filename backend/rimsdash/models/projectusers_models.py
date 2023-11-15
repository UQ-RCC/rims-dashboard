from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship

from .base_model import Base, ProjectRight

class ProjectUsersModel(Base):
    """
    junction table linking user + system with rights level
    """
    __tablename__ = 'rdprojectusers'
    username = Column(String, ForeignKey('rduser.username'), primary_key=True)
    project_id = Column(Integer, ForeignKey('rdproject.id'), primary_key=True)
    status = Column(Enum(ProjectRight), primary_key=False, index=False, nullable=False)
    user = relationship("UserModel", back_populates="project_rights")
    project = relationship("ProjectModel", back_populates="user_rights")


"""
to use:
    junction = session.query(JunctionTable).filter_by(table1_id=table1_id, table2_id=table2_id).first()

    if junction.status == 'OK':
        print('yes')
"""