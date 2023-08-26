from enum import Enum


import rimsboard.rims as rims
import rimsboard.utils as utils
import rimsboard.usergather as gather

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

    user_dict = gather.get_user_details(user_login)

    user_projects = rims.get_user_projects(user_login)
    
    rights_df = gather.get_user_rights_df(user_login)

    labright_array = extract_labrights_array(rights_df)

    #try to find user name in project titles
    #   if found use first match
    #   if not found, use last in list (ie. most recent)
    for proj in user_projects:
        project_df = gather.gather_projectdetails(proj)
        project_dict = project_df.to_dict('records')[0]

        user_name = utils.cleanup_user_name(user_name)
        user_name = utils.reorder_user_name(user_name)

        if user_name.lower() in project_dict['ProjectName'].lower() and bool(project_dict['Active'])==True:
            break

    project_array = extract_project_array(project_df)

    core_array = extract_core_array(user_login, project_array)

    print(f"MOD core: {core_array}")
    print(f"access: {labright_array}")
    print(f"proj: {project_array}")    

    result = [core_array, labright_array, project_array]

    return result
    #return core_array, labright_array, project_array


def extract_core_array(user_login, project_array):

    result = [ ISTATES.off, ISTATES.off ]

    if not user_login is None:
        result[0] = ISTATES.ok

    #set ok if
    #   project is active, has account, has ohs, has rdm, and is phase 2
    if project_array[0:4] == [ ISTATES.ok, ISTATES.ok, ISTATES.ok, ISTATES.ok ] \
        and project_array[6] == ISTATES.ok:
        result[1] = ISTATES.ok

    #set in-progress if
    #   any of the above are ok
    elif project_array[0:8] == [ ISTATES.off, ISTATES.off, ISTATES.off, ISTATES.off, ISTATES.off, ISTATES.off, ISTATES.off, ISTATES.off ]:
        result[1] = ISTATES.fail
    else:
        result[1] = ISTATES.warn

    return result


def extract_labrights_array(df):
    """
    produce a list of rights by lab
    """

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

            if access_level in ['N', 'A', 'S']:
                result[i] = ISTATES.ok
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
                result[i] = ISTATES.ok

        except:
            pass

    return result


def extract_project_array(df):
    
                #active, account, ohs, rdm, p0, p1, p2, p3
    result = [ ISTATES.off, ISTATES.off, ISTATES.off, ISTATES.off, ISTATES.off, ISTATES.off, ISTATES.off, ISTATES.off ]

    if len(df) == 0:
        return result

    phase = df['Phase'].iloc[0]
    OFFSET=4

    if phase == 0:
        result[OFFSET+0] = ISTATES.fail
    elif phase == 1:
        result[OFFSET+1] = ISTATES.warn
    elif phase == 2:
        result[OFFSET+2] = ISTATES.ok
    elif phase == 3:
        result[OFFSET+3] = ISTATES.fail   

    if bool(df['Active'].iloc[0]) == True:
        result[0] = ISTATES.ok
    
    if not df['Bcode'].iloc[0] is None:
        result[1] = ISTATES.ok    

    result[2] = ISTATES.ok    #TO-DO

    result[3] = ISTATES.ok    #TO-DO

    return result