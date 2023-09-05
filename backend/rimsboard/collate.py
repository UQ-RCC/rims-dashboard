from enum import Enum
from flask import jsonify

import rimsboard.rims as rims
import rimsboard.utils as utils
import rimsboard.usergather as gather

"""
class IState():
    def __init__(self):
        #base
        self.off = 0
        #good
        self.work = 1
        self.ok = 2
        self.active = 3
        #bad
        self.warn = 11
        self.fail = 12
        self.na = -1
"""


class State():
    def __init__(self, label: str, value: str):
        self.label = label
        self.value = value
    def as_dict(self):
        return { 'label': self.label, 'value': self.value}



class State_group():
    def __init__(self, label: str, states:list = []):
        self.label = label
        self.states = states

    def add(self, state: State):
        self.states.append(state)

    def assign(self, label: str, value):
        for i in self.states:
            if i.label == label:
                i.value = value

    def as_dict(self):
        value_array = [] 
        for i in self.states:
            value_array.append(i.as_dict())

        return { 'label': self.label, 'value': self.value_array }



class IState():
    """
    collection of valid states to hand back
    """
    def __init__(self):
        #standard--------
        self.off = 'off'
        self.incomplete = 'incomplete'
        self.waiting = 'waiting'
        self.waiting_external = 'waiting_external'
        self.ready = 'ready'
        self.extended = 'extended'
        self.disabled = 'disabled'
        #error------------
        self.warn = 'warn'
        self.fail = 'fail'
        self.na = 'na'

ISTATES = IState()  

USER_ACCESS_DEFAULT =   State('access',
                            [
                                State('aibn', ISTATES.off),
                                State('hawken', ISTATES.off),
                                State('chemistry', ISTATES.off),
                                State('qbp', ISTATES.off),
                            ]
                        )

USER_OUTPUT_DEFAULT =   State('user',
                            [ 
                                State('active', ISTATES.off),
                                State('account', ISTATES.off),
                                USER_ACCESS_DEFAULT,
                            ]
                        )

PROEJCT_OUTPUT_DEFAULT =    State('project',
                                [
                                    State('overall', ISTATES.off),
                                    State('active', ISTATES.off),
                                    State('financial', ISTATES.off),
                                    State('OHS', ISTATES.off),
                                    State('RDM', ISTATES.off),
                                    State('phase', ISTATES.off),
                                ]
                            )


#rims codes for each lab & access-level
RIMS_LAB_CODES_PRIME = [ 82, 89, 87, -1]
RIMS_LAB_CODES_AH = [ 83, 88, 86, 84]
                #Ha, AIBN, Chem, QBP

def populate_userdropdown():
    """
    generate a list of dicts for user logins and names for dash dropdown
    """
    uid_list, name_list = gather.gather_userlists()

    name_list, uid_list = utils.sort_paired(name_list, uid_list)

    options=[]

    for i, uid in enumerate(uid_list):
        options.append({'search': f"{name_list[i]} ({uid_list[i]})", 'ulogin': uid_list[i], 'name': name_list[i]})
    
    return options


"""
TO-DO:
    really need separate functions

    state_from_user
    - retrieve primary project
    - (retrieve all projects)
    
    state_from_project
    - retrieve primary user
    - (retrieve all users)

    all carrying same info, but recombined
    preferably querying local DB, not rims

    for now, just consider dash_state as state_from_user

"""



def state_from_user(user_login):
    """
    compile dashboard state for this user
    """
    user_dict = gather.get_user_details(user_login)

    user_name = user_dict['name']
    user_name_clean = utils.cleanup_user_name(user_name)
    user_name_first_last = utils.reorder_user_name(user_name_clean)

    user_projects = rims.get_user_projects(user_login)
    
    rights_df = gather.get_user_rights_df(user_login)

    user_result = collate_user(rights_df)

    print(user_result)

    #try to find user name in project titles

    oldest=None
    oldest_active=None
    found=False

    if not user_projects == [-1]:
        for proj in user_projects:
            project_df = gather.gather_projectdetails(proj)
            try:
                project_dict = project_df.to_dict('records')[0]
            except:
                #dict conversion will fail on inaccessible projects (eg. 1995)
                #skip these if present
                continue

            #   if found use first match (ie. oldest)
            #   if not found as lead, use oldest active project containing user
            #   if no active projects at all, use oldest project

            if oldest is None:
                oldest = project_df

            if oldest_active is None and \
                bool(project_dict['Active'])==True and project_dict['Phase']==2:

                oldest_active = project_df

            if ( user_name_first_last.lower() in project_dict['ProjectName'].lower() \
                or user_name_clean.lower() in project_dict['ProjectName'].lower() )\
                and bool(project_dict['Active'])==True and project_dict['Phase']==2:

                project_df = project_df
                found=True
                break

        if found == True:
            pass        
        elif oldest_active is not None:
            project_df = oldest_active
        elif oldest is not None:
            project_df = oldest    
        else:
            raise ValueError("Unexpected value for project DF")        

        project_result = collate_project(project_df)
    else:
        #return empty array
        project_result = PROEJCT_OUTPUT_DEFAULT

    #to-do:
    #   project.OHS using user_result and project_result
    #   loop through multiple projects

    project_result_array = [ project_result ]

    #dict
    result = { 'user': user_result, 'projects': project_result_array}

    print(f"result: {result}")

    return result
    #TODO test cases:
    #   ok project
    #   no projects
    #   ghost project (ie. 1995)
    #   only ghost project
    #   only bad projects
    #   CHECK alafif failing


def collate_user(df):
    """
    produce a list of rights by lab
    """


    result = USER_OUTPUT_DEFAULT

    _keys=list(result['access'].keys())

    if len(df) == 0:
        return result

    for i, code in enumerate(RIMS_LAB_CODES_PRIME):
        access_level = None
        row = df.loc[df['systemid'] == code]['access_level']

        try:
            access_level = row.iloc[0]

            if access_level in ['N', 'A', 'S']:
                result['access'][_keys[i]] = ISTATES.ready
            elif access_level == 'D':
                result['access'][_keys[i]] = ISTATES.disabled
            else:
                result['access'][_keys[i]] = ISTATES.off
        
        except:
            print(f'unexpected access {access_level} for lab: {i}, {code}')
            result['access'][_keys[i]] = ISTATES.off

    for i, code in enumerate(RIMS_LAB_CODES_AH):
        row = df.loc[df['systemid'] == code]['access_level']

        try:
            access_level = row.iloc[0]

            if access_level in ['N', 'A', 'S']:
                result['access'][_keys[i]] = ISTATES.extended

        except:
            pass
    
    #TO-DO get this from df
    result['account'] = ISTATES.ready

    #calc overall from other states
    if result['account'] == ISTATES.ready and ( 
        result['access']['aibn'] == ISTATES.ready or result['access']['aibn'] == ISTATES.extended or \
        result['access']['hawken'] == ISTATES.ready or result['access']['hawken'] == ISTATES.extended or \
        result['access']['chemistry'] == ISTATES.ready or result['access']['hawken'] == ISTATES.extended or \
        result['access']['qbp'] == ISTATES.ready or result['access']['hawken'] == ISTATES.extended
    ):
        result['overall'] = ISTATES.ready
    else:
        result['overall'] = ISTATES.off

    return result


def collate_project(df):
    
    result = PROEJCT_OUTPUT_DEFAULT

    try:
        if len(df) == 0:
            return result

        phase = df['Phase'].iloc[0]
        OFFSET=4

        if phase == 0:
            result['phase'] = ISTATES.waiting
        elif phase == 1:
            result['phase'] = ISTATES.waiting
        elif phase == 2:
            result['phase'] = ISTATES.ready
        elif phase == 3:
            result['phase'] = ISTATES.disabled   

        if bool(df['Active'].iloc[0]) == True:
            result['active'] = ISTATES.ready
        
        if not df['Bcode'].iloc[0] is None:
            result['financial'] = ISTATES.ready    

        #if has rights in any lab
        #or is fee-for-service
        result['OHS'] = ISTATES.ready    #TO-DO

        #if has an RDM assigned
        result['RDM'] = ISTATES.ready    #TO-DO

        #set overall from other states
        #bugged?
        all_ready = result['active'] == ISTATES.ready and \
            result['financial'] == ISTATES.ready and \
            result['OHS'] == ISTATES.ready and \
            result['RDM'] == ISTATES.ready and \
            result['phase'] == ISTATES.ready

        if all_ready:
            #endif
            result['overall'] = ISTATES.ready
        else:
            result['overall'] = ISTATES.off

    finally:
        return result