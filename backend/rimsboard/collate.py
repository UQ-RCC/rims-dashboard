from enum import Enum
from flask import jsonify

import rimsboard.rims as rims
import rimsboard.utils as utils
import rimsboard.usergather as gather

from logic import ISTATES, IndicatorState, IndicatorStateGroup

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


#rims codes for each lab & access-level
RIMS_LAB_CODES_PRIME = [ 82, 89, 87, -1]
RIMS_LAB_CODES_AH = [ 83, 88, 86, 84]
                #Ha, AIBN, Chem, QBP
RIMS_LAB_KEYS = [ 'aibn', 'hawken', 'chemistry', 'qbp']


USER_TEMPLATE =   IndicatorStateGroup('user',
                            [ 
                                IndicatorState('overall', ISTATES.off),
                                IndicatorState('account', ISTATES.off),
                                IndicatorState(RIMS_LAB_KEYS[0], ISTATES.off),
                                IndicatorState(RIMS_LAB_KEYS[1], ISTATES.off),
                                IndicatorState(RIMS_LAB_KEYS[2], ISTATES.off),
                                IndicatorState(RIMS_LAB_KEYS[3], ISTATES.off),
                            ]
                        )

PROJECT_TEMPLATE =    IndicatorStateGroup('project',
                                [
                                    IndicatorState('overall', ISTATES.off),
                                    IndicatorState('active', ISTATES.off),
                                    IndicatorState('financial', ISTATES.off),
                                    IndicatorState('OHS', ISTATES.off),
                                    IndicatorState('RDM', ISTATES.off),
                                    IndicatorState('phase', ISTATES.off),
                                ]
                            )




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
        project_result = PROJECT_TEMPLATE

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

    user_result = USER_TEMPLATE
    _keys=RIMS_LAB_KEYS

    if len(df) == 0:
        return user_result

    for i, code in enumerate(RIMS_LAB_CODES_PRIME):
        access_level = None
        row = df.loc[df['systemid'] == code]['access_level']

        try:
            access_level = row.iloc[0]

            if access_level in ['N', 'A', 'S']:
                user_result.assign([_keys[i]], ISTATES.ready)
            elif access_level == 'D':
                user_result.assign([_keys[i]], ISTATES.disabled)
            else:
                user_result.assign([_keys[i]], ISTATES.off)
        
        except:
            print(f'unexpected access {access_level} for lab: {i}, {code}')
            user_result.assign([_keys[i]], ISTATES.na)

    for i, code in enumerate(RIMS_LAB_CODES_AH):
        row = df.loc[df['systemid'] == code]['access_level']

        try:
            access_level = row.iloc[0]

            if access_level in ['N', 'A', 'S']:
                user_result.assign([_keys[i]], ISTATES.extended)

        except:
            pass
    
    #TO-DO get this from df
    user_result.assign('account', ISTATES.ready)

    #calc overall from other states
    if user_result.get('account') == ISTATES.ready and ( 
        user_result.get('aibn') == ISTATES.ready or user_result.get('aibn') == ISTATES.extended or \
        user_result.get('hawken') == ISTATES.ready or user_result.get('hawken') == ISTATES.extended or \
        user_result.get('chemistry') == ISTATES.ready or user_result.get('chemistry') == ISTATES.extended or \
        user_result.get('qbp') == ISTATES.ready or user_result.get('qbp') == ISTATES.extended
    ):
        user_result.assign('overall', ISTATES.ready)
    else:
        user_result.assign('overall', ISTATES.off)

    return user_result


def collate_project(df):
    
    project_result = PROJECT_TEMPLATE

    try:
        if len(df) == 0:
            return project_result

        phase = df['Phase'].iloc[0]
        OFFSET=4

        if phase == 0:
            project_result.assign('phase', ISTATES.waiting)
        elif phase == 1:
            project_result.assign('phase', ISTATES.waiting)
        elif phase == 2:
            project_result.assign('phase', ISTATES.ready)
        elif phase == 3:
            project_result.assign('phase', ISTATES.disabled)

        if bool(df['Active'].iloc[0]) == True:
            project_result.assign('active', ISTATES.ready)
        
        if not df['Bcode'].iloc[0] is None:
            project_result.assign('financial', ISTATES.ready)

        #if has rights in any lab
        #or is fee-for-service
        project_result.assign('OHS', ISTATES.ready)    #TO-DO

        #if has an RDM assigned
        project_result.assign('RDM', ISTATES.ready)    #TO-DO

        #set overall from other states
        #bugged?
        all_ready = \
            project_result.get('active') == ISTATES.ready and \
            project_result.get('financial') == ISTATES.ready and \
            project_result.get('OHS') == ISTATES.ready and \
            project_result.get('RDM') == ISTATES.ready and \
            project_result.get('phase') == ISTATES.ready

        if all_ready:
            #endif
            project_result.assign('overall', ISTATES.ready)
        else:
            project_result.assign('overall', ISTATES.off)

    finally:
        return project_result