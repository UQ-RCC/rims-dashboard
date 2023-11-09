from rimsdash.models import IStatus, UserStateModel, ProjectStateModel
from rimsdash.schemas import UserFullSchema, ProjectFullSchema, UserStateCreateSchema, ProjectStateCreateSchema

import rimsdash.utils as utils

#rims codes for each lab & access-level
#NB: order MUST match
RIMS_LAB_KEYS = [ 'hawken', 'aibn', 'chem', 'qbp']
RIMS_LAB_CODES_PRIME = [ 82, 89, 87, 182]
RIMS_LAB_NAMES_PRIME = [
    "HAWKEN LAB ACCESS 9AM",
    "AIBN LAB ACCESS 9AM",
    "CHEMISTRY LAB ACCESS 9AM",
    "QBP LAB ACCESS 9AM",
]
RIMS_LAB_CODES_AH = [ 83, 88, 86, 84]
RIMS_LAB_NAMES_AH = [
    "HAWKEN LAB ACCESS 24",
    "AIBN LAB ACCESS 24",
    "CHEMISTRY LAB ACCESS 24",
    "QBP LAB ACCESS 24",
]
RIMS_LAB_TYPES = [
    "Z_HAWKEN LAB", "Z_AIBN LAB", "Z_CHEMISTRY LAB LEVEL 2", "Z_QBP LAB"
]
#extra prime: "QBP UQROCX LAB ACCESS 9AM": 163
#extra AH: "QBP CRYO EM AFTER HOURS":85, "QBP UQROCX LAB ACCESS 24":164
#extra types: [ "MASS SPEC LAB", "Z_CHEM ENG LAB", "Z_CHEMISTRY LAB LEVEL 7" ]

def get_rims_key(code: int):
    for i in range(len(RIMS_LAB_KEYS)):
        if code == RIMS_LAB_CODES_PRIME[i] or code == RIMS_LAB_CODES_AH[i]:
            return RIMS_LAB_KEYS[i]
    raise ValueError(f"code {code} not found in lab code lists")


def process_user(user: UserFullSchema) -> UserStateCreateSchema:
    """
    generate status result from user data
    """    
    pass

def process_project(project: ProjectFullSchema) -> ProjectStateCreateSchema:
    """
    generate status result from project data
    """
    state = ProjectStateCreateSchema(id = project.id)

    try:
        if project.phase == 0:
            state.phase = IStatus.waiting
        elif project.phase == 1:
            state.phase = IStatus.waiting
        elif project.phase == 2:
            state.phase = IStatus.ready
        elif project.phase == 3:
            state.phase = IStatus.disabled
        else:
            state.phase = IStatus.fail

        if project.active == True:
            state.active = IStatus.ready
        else:
            state.active = IStatus.disabled

        if project.bcode is not None:
            state.billing = IStatus.ready
        else:
            state.billing = IStatus.disabled
            ##FUTURE: check financial report for chartstring validity

        #FUTURE: if has rights in any lab
        #or is fee-for-service
        state.ohs = state.phase    #TO-DO

        #if has an RDM assigned
        if project.qcollection is not None:
            state.rdm = IStatus.ready    #TO-DO
        else:
            state.rdm = IStatus.disabled

        #set overall from other states
        all_ready = \
            state.active == IStatus.ready and \
            state.billing == IStatus.ready and \
            state.ohs == IStatus.ready and \
            state.rdm == IStatus.ready and \
            state.phase == IStatus.ready

        if all_ready:
            state.ok = IStatus.ready
        else:
            state.ok = IStatus.fail

    finally:
        return state
