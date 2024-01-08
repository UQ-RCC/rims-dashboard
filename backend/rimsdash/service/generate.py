import rimsdash.crud as crud
import rimsdash.schemas as schemas

def generate_projects(db):
    __projects = crud.project.get_all(db)

    for project in __projects:
        yield project