from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

import rimsdash.crud as crud
from rimsdash.models.project_models import ProjectModel

def filter_by_title(db: Session, *, substring: str) -> Optional[list[ProjectModel]]:
    projects = crud.project.get_by_title(db, substring=substring)
    return projects

def filter_by_group(db: Session, *, substring: str) -> Optional[list[ProjectModel]]:
    projects = crud.project.get_by_group(db, substring=substring)
    return projects

def get_by_id(db: Session, *, project_id: int) -> Optional[ProjectModel]:
    project = crud.project.get(db, project_id)
    return project

def filter_projects_by_username(db: Session, *, substring: str) -> Optional[list[ProjectModel]]:
    """
    find projects associated with user via username substring
    """
    users = []
    projects=[]

    user = crud.user.get(db, substring)

    if user:
        users = [user]
    else:
        users = crud.user.get_by_username_substring(db, substring=substring)
    
    for user in users:
        __projects=crud.projectuser.get_projects_by_username(db, username=user.username)

        #check for duplicates and append
        for __project in __projects:
            if __project not in projects:
                projects.append(__project)

    return projects

def filter_projects_by_user_fullname(db: Session, *, substring: str) -> Optional[list[ProjectModel]]:
    """
    find projects associated with user via user full name substring
    """
    projects=[]

    users = crud.user.get_by_name(db, substring=substring)
    
    for user in users:
        __projects = crud.projectuser.get_projects_by_username(db, username=user.username)
        
        #check for duplicates and append
        for __project in __projects:
            if __project not in projects:
                projects.append(__project)

    return projects

def filter_projects_by_user_allnames(db: Session, *, substring: str) -> Optional[list[ProjectModel]]:
    """
    find projects associated with user via username OR full name substrings
    """
    projects = filter_projects_by_username(db, substring=substring)

    __projects = filter_projects_by_user_fullname(db, substring=substring)

    #check for duplicates and combine
    for __project in __projects:
        if __project not in projects:
            projects.append(__project)

    return projects