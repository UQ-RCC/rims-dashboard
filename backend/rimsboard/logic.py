import copy
from rimsboard.statelogic import Istate, UserState, UserStateLabels, ProjectState, ProjectStateLabels

import rimsboard.utils as utils

#rims codes for each lab & access-level
RIMS_LAB_KEYS = [ 'aibn', 'hawken', 'chem', 'qbp']
RIMS_LAB_CODES_PRIME = [ 82, 89, 87, -1]
RIMS_LAB_CODES_AH = [ 83, 88, 86, 84]
                #Ha, AIBN, Chem, QBP


def get_rims_key(code: int):
    for i in range(4):
        if code == RIMS_LAB_CODES_PRIME[i] or code == RIMS_LAB_CODES_AH[i]:
            return RIMS_LAB_KEYS[i]
    raise ValueError(f"code {code} not found in rims lab code lists")


def collate_user(user_rights):
    """
    produce a list of rights by lab
    """

    user_state = UserState()

    for key in user_rights:
        
        if int(key) in RIMS_LAB_CODES_PRIME:

            for i, code in enumerate(RIMS_LAB_CODES_PRIME):    
                current_lab = get_rims_key(code)        

                if int(key) == code:
                    access_level = user_rights[key]

                    if access_level in ['N', 'A', 'S']:
                        user_state.assign_by_lab(current_lab, Istate.ready)
                    elif access_level == 'D':
                        user_state.assign_by_lab(current_lab, Istate.disabled)
                    else:
                        print(f'unexpected access {access_level} for lab: {i}, {code}')                
                        user_state.assign_by_lab(current_lab, Istate.na)   

        if int(key) in RIMS_LAB_CODES_AH:

            for i, code in enumerate(RIMS_LAB_CODES_AH):    
                current_lab = get_rims_key(code)        

                if int(key) == code:
                    access_level = user_rights[key]

                    if access_level in ['N', 'A', 'S']:
                        user_state.assign_by_lab(current_lab, Istate.extended)
                    else:
                        pass               
    
    #TO-DO get this from df
    user_state.active = Istate.ready

    #calc overall from other states
    if user_state.active == Istate.ready and \
            any((labstate == Istate.ready or labstate == Istate.extended) for labstate in user_state.labs_as_list()):

        user_state.total = Istate.ready
    else:
        user_state.total = Istate.off

    return user_state


def collate_project(df):
    
    project_state = ProjectState()

    try:
        if len(df) == 0:
            return project_state

        phase = df['Phase'].iloc[0]

        if phase == 0:
            project_state.phase = Istate.waiting
        elif phase == 1:
            project_state.phase = Istate.waiting
        elif phase == 2:
            project_state.phase = Istate.ready
        elif phase == 3:
            project_state.phase = Istate.disabled

        if bool(df['Active'].iloc[0]) == True:
            project_state.active = Istate.ready
        
        if not df['Bcode'].iloc[0] is None:
            project_state.billing = Istate.ready
            #future: check financial report for chartstring validity

        #if has rights in any lab
        #or is fee-for-service
        project_state.ohs = Istate.ready    #TO-DO

        #if has an RDM assigned
        project_state.rdm = Istate.ready    #TO-DO

        #set overall from other states
        all_ready = \
            project_state.active == Istate.ready and \
            project_state.billing == Istate.ready and \
            project_state.ohs == Istate.ready and \
            project_state.rdm == Istate.ready and \
            project_state.phase == Istate.ready

        if all_ready:
            project_state.total = Istate.ready
        else:
            project_state.total = Istate.off

    finally:
        return project_state


def collate_project_dict(project_dict):
    
    project_state = ProjectState()

    try:
        if not (isinstance(project_dict, dict)):
            return project_state

        phase = project_dict['Phase']

        if phase == 0:
            project_state.phase = Istate.waiting
        elif phase == 1:
            project_state.phase = Istate.waiting
        elif phase == 2:
            project_state.phase = Istate.ready
        elif phase == 3:
            project_state.phase = Istate.disabled
        else:
            project_state.phase = Istate.fail

        if utils.str2bool(project_dict['Active']) == True:
            project_state.active = Istate.ready
        else:
            project_state.active = Istate.disabled

        if not project_dict['Bcode'] is None:
            project_state.billing = Istate.ready
            #future: check financial report for chartstring validity

        #if has rights in any lab
        #or is fee-for-service
        project_state.ohs = project_state.phase    #TO-DO

        #if has an RDM assigned
        project_state.rdm = Istate.ready    #TO-DO

        #set overall from other states
        all_ready = \
            project_state.active == Istate.ready and \
            project_state.billing == Istate.ready and \
            project_state.ohs == Istate.ready and \
            project_state.rdm == Istate.ready and \
            project_state.phase == Istate.ready

        if all_ready:
            project_state.total = Istate.ready
        else:
            project_state.total = Istate.fail

    finally:
        return project_state