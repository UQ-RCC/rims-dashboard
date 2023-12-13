import copy

from rimsdash.models import IStatus, UserStateModel, ProjectStateModel, SystemRight

from rimsdash.schemas import UserForStateCheckSchema, UserStateCreateSchema, ProjectStateCreateSchema, ProjectForStateCheckSchema


import rimsdash.config as config
import rimsdash.utils as utils


EXTERNAL_AFFILIATIONS = config.get_csv_list('manual', 'external_affiliations')

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
PITSCHI_SYSTEM_ID = 132

RIGHTS_OK = [ SystemRight.novice, SystemRight.autonomous, SystemRight.superuser ]
#extra prime: "QBP UQROCX LAB ACCESS 9AM": 163
#extra AH: "QBP CRYO EM AFTER HOURS":85, "QBP UQROCX LAB ACCESS 24":164
#extra types: [ "MASS SPEC LAB", "Z_CHEM ENG LAB", "Z_CHEMISTRY LAB LEVEL 7" ]



def get_rims_key(code: int):
    for i in range(len(RIMS_LAB_KEYS)):
        if code == RIMS_LAB_CODES_PRIME[i] or code == RIMS_LAB_CODES_AH[i]:
            return RIMS_LAB_KEYS[i]
    raise ValueError(f"code {code} not found in lab code lists")


def recursive():
    """
    for project in projects:
        __user_ok = IState.fail

        if project.type == "Fee for service":
            __user_ok = IState.ok
        else:
            __found_user = False         

            for user in project_users
                if user.admin == False:
                    __found_user = True
                    if user.user_state.ok == IState.ok
                        __user_ok = True
            
            if not __found_user:
                for user in project_users:
                    if lower(user.name) in lower(project.title) :
                        __found_user = True
                        if user.user_state.ok == IState.ok
                            __user_ok = True                                   
            
            if not __found_user:        
                logger.warn("No user found for project {project.id}")

        project.project_state.user_ok = __user_ok
    """
    pass


def postprocess_project(user: UserForStateCheckSchema):
    pass


def process_user(user: UserForStateCheckSchema) -> UserStateCreateSchema:
    """
    generate status result from user data
    """    
    state = UserStateCreateSchema(username=user.username)

    #access rights:
    for _usersystem in user.system_rights:

        if _usersystem.status in RIGHTS_OK:

            #primetime
            if _usersystem.system_id == RIMS_LAB_CODES_PRIME[0]:
                state.access_hawken = IStatus.ready
            elif _usersystem.system_id == RIMS_LAB_CODES_PRIME[1]:
                state.access_aibn = IStatus.ready
            elif _usersystem.system_id == RIMS_LAB_CODES_PRIME[2]:
                state.access_chem = IStatus.ready        
            elif _usersystem.system_id == RIMS_LAB_CODES_PRIME[3]:
                state.access_qbp = IStatus.ready
            #after hours
            elif _usersystem.system_id == RIMS_LAB_CODES_AH[0]:
                state.access_hawken = IStatus.extended
            elif _usersystem.system_id == RIMS_LAB_CODES_AH[1]:
                state.access_aibn = IStatus.extended
            elif _usersystem.system_id == RIMS_LAB_CODES_AH[2]:
                state.access_chem = IStatus.extended        
            elif _usersystem.system_id == RIMS_LAB_CODES_AH[3]:
                state.access_qbp = IStatus.extended

            #pitschi
            elif _usersystem.system_id == PITSCHI_SYSTEM_ID:
                state.access_pitschi = IStatus.ok

    #admin pitschi cheat
    if user.admin == True:
        state.access_pitschi = IStatus.ok

    if user.active == True:
        state.active = IStatus.ready
    else:
        state.active = IStatus.disabled
    
    if state.active == IStatus.ready and \
        state.access_pitschi == IStatus.ok \
        and any(
            (labstate == IStatus.ready or labstate == IStatus.extended) for \
            labstate in [ state.access_hawken, state.access_aibn, state.access_chem, state.access_qbp ]
    ):
        state.ok = IStatus.ready
    else:
        state.ok = IStatus.fail
    
    return state



def process_project(project: ProjectForStateCheckSchema) -> ProjectStateCreateSchema:
    """
    generate status result from project data
    """
    state = ProjectStateCreateSchema(project_id = project.id)

    try:
        #phase
        if project.phase == 0:
            state.phase = IStatus.disabled
        elif project.phase == 1:
            state.phase = IStatus.waiting
        elif project.phase == 2:
            state.phase = IStatus.waiting
        elif project.phase == 3:
            state.phase = IStatus.ready
        elif project.phase == 4:
            state.phase = IStatus.disabled            
        else:
            state.phase = IStatus.fail

        #activity status
        if project.active == True:
            state.active = IStatus.ready
        else:
            state.active = IStatus.disabled

        
        #billing
        if project.affiliation in EXTERNAL_AFFILIATIONS:
            state.billing = IStatus.ready
        else:
            try:                
                if project.project_account[0].valid == True:
                    state.billing = IStatus.ready
                elif project.project_account[0].valid == False:
                    state.billing = IStatus.fail
            except:
                state.billing = IStatus.disabled                        
            

        #FUTURE: if has rights in any lab
        #or is fee-for-service
        state.ohs = state.phase    #TO-DO

        #if has an RDM assigned
        if project.qcollection is not None and not project.qcollection == '':
            state.rdm = IStatus.ready    
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
