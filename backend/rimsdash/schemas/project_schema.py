from typing import Optional, ForwardRef

from .base_schema import BaseSchema

#use forward refs for circular deps

ProjectStateOutSchema=ForwardRef('ProjectStateOutSchema')
ProjectUsersOutSchema=ForwardRef('ProjectUsersOutSchema')
ProjectUsersOutFromProjectSchema=ForwardRef('ProjectUsersOutFromProjectSchema')


class ProjectBaseSchema(BaseSchema):
    id: int
    title: str
    phase: int
    active: bool = False   
    type: str
    group: str
    coreid: int = 2    
    bcode: str = None
    affiliation: str = None
    description: str = None

    class Config:
        orm_mode = True

#complete DB schema with all fields
class ProjectFullSchema(ProjectBaseSchema):
    qcollection: Optional[str] = None
    status: Optional[str] = None
    project_state: Optional[list[ProjectStateOutSchema]]
    user_rights: Optional[list[ProjectUsersOutSchema]]
    ...


# Properties on creation
class ProjectCreateSchema(ProjectBaseSchema):
    ...

# Additional properties on initialise
class ProjectInitDetailsSchema(BaseSchema):
    id: int
    qcollection: str = None
    status: str = None

    class Config:
        orm_mode = True

# Properties on update
class ProjectUpdateSchema(ProjectBaseSchema):
    ...

class ProjectReceiveSchema(ProjectBaseSchema):
    ...    



#export schema
#---------------
#   naming convention:  
#       out > info > refs > extended > full

class ProjectOutSchema(ProjectBaseSchema):
    """
    base export, no references
    """    
    ...
    qcollection: str = None
    status: str = None

class ProjectOutWithStateSchema(ProjectOutSchema):
    """

    FUTURE: consider merging this with ProjectOutSchema 
        and creating ProjectNoRefs for ProjectStateSchema only
    """
    ...
    project_state: Optional[list[ProjectStateOutSchema]]

class ProjectOutRefsSchema(ProjectOutSchema):
    """
    include users and user state
    """ 
    ...
    project_state: Optional[list[ProjectStateOutSchema]]    
    user_rights: Optional[list[ProjectUsersOutFromProjectSchema]]  



#import the circular deps and update forward
from .projectusers_schema import ProjectUsersOutSchema, ProjectUsersOutFromProjectSchema
from .project_state_schema import ProjectStateOutSchema


ProjectFullSchema.update_forward_refs()
ProjectOutWithStateSchema.update_forward_refs()
ProjectOutRefsSchema.update_forward_refs()


"""

PROJECT TABLE:

search by: user


project_for_table
    id
    title
    group
    *projectuser
        *user
            username
            name
    *state
   










project
	*local
	state
	projectuser
		user
			*local
			state


search by: project user

user
	*local
	state
	projectuser
		project
			*local
			state
	systemuser
		system
			*local



user_state
	*local
	user
		*local
		state
		projectuser
			project
				*local
				state
		systemuser
			system
				*local
"""