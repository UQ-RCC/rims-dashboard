from enum import Enum


import backend.rims as rims
import backend.utils as utils
import backend.usergather as gather

class IState():
    def __init__(self):
        #base
        self.off = 0
        #good
        self.work = 1
        self.on = 2
        self.full = 3
        #bad
        self.warn = 11
        self.fail = 12
        self.na = -1

ISTATES = IState()

def populate_userdropdown():
    """
    generate a list of dicts for user logins and names for dash dropdown
    """
    uid_list, name_list = gather.gather_userlists()

    name_list, uid_list = utils.sort_paired(name_list, uid_list)

    options=[]

    for i, uid in enumerate(uid_list):
        options.append({'label': f"{name_list[i]} ({uid_list[i]})", 'value': uid_list[i], 'search': name_list[i]})
    
    return options


def dash_state(user_login):

    user_projects = rims.get_user_projects(user_login)
    
    rights_df = gather.get_user_rights_df(user_login)

    project_df = gather.gather_projectdetails(user_projects[0])

    labright_array = extract_labrights_array(rights_df)

    project_array = extract_project_array(project_df)

    core_array = extract_core_array(user_login, project_array)

    print(f"core: {core_array}")
    print(f"access: {labright_array}")
    print(f"proj: {project_array}")    

    return core_array, labright_array, project_array


def extract_core_array(user_login, project_array):

    result = [ ISTATES.off, ISTATES.off ]

    if not user_login is None:
        result[0] = ISTATES.on

    #set ok if
    #   project is active, has account, has ohs, has rdm, and is phase 2
    if project_array[0:3] == [ ISTATES.on, ISTATES.on, ISTATES.on, ISTATES.on ] \
        and project_array[6] == ISTATES.on:
        result[1] = ISTATES.on

    #set in-progress if
    #   any of the above are ok
    elif project_array[0:8] == [ ISTATES.off, ISTATES.off, ISTATES.off, ISTATES.off, ISTATES.off, ISTATES.off, ISTATES.off, ISTATES.off ]:
        result[1] = ISTATES.off
    else:
        result[1] = ISTATES.work

    return result


def extract_project_array(df):
    
                #active, account, ohs, rdm, p0, p1, p2, p3
    result = [ ISTATES.off, ISTATES.off, ISTATES.off, ISTATES.off, ISTATES.off, ISTATES.off, ISTATES.off, ISTATES.off ]

    if len(df) == 0:
        return result

    phase = df['Phase'].iloc[0]
    OFFSET=4
    for i in range(0,4):
        if phase == i:
            result[i+OFFSET] = ISTATES.on
        else:
            result[i+OFFSET] = ISTATES.off
    
    if bool(df['Active'].iloc[0]) == True:
        result[0] = ISTATES.on
    
    if not df['Bcode'].iloc[0] is None:
        result[1] = ISTATES.on    

    result[2] = ISTATES.on    #TO-DO

    result[3] = ISTATES.on    #TO-DO

    return result


def extract_labrights_array(df):
    """
    produce a list of rights by lab
    """

    #TO-DO check business logic here
    #not certain if we are using N in A/H or A in Prime to denote after-hours

                    #Ha, AIBN, Chem, QBP
    LAB_CODES_PRIME = [ 82, 89, 87, -1]
    LAB_CODES_AH = [ 83, 88, 86, 84]

    result = [ ISTATES.off, ISTATES.off, ISTATES.off, ISTATES.off ]

    if len(df) == 0:
        return result

    for i, code in enumerate(LAB_CODES_PRIME):
        row = df.loc[df['systemid'] == code]['access_level']

        try:
            access_level = row.iloc[0]

            if access_level == 'N':
                result[i] = ISTATES.on
            elif access_level in ['A', 'S']:
                result[i] = ISTATES.full
            elif access_level == 'D':
                result[i] = ISTATES.fail
            else:
                result[i] = ISTATES.off
        
        except:
            result[i] = 0

    for i, code in enumerate(LAB_CODES_AH):
        row = df.loc[df['systemid'] == code]['access_level']

        try:
            access_level = row.iloc[0]

            if access_level in ['N', 'A', 'S']:
                result[i] = ISTATES.full

        except:
            pass

    return result



