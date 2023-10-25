import copy

from enum import Enum
from dataclasses import dataclass, asdict, field


import rimsdash.rims as rims
import rimsdash.utils as utils
import rimsdash.usergather as gather

import rimsdash.logic as logic
from rimsdash.statelogic import Istate, UserState, UserStateLabels, ProjectState, ProjectStateLabels

DEFAULT_USER_METADATA = {
    'id': 2,
    'login': 'N/A',
    'name': '( Not found )',
    'email': '( Not found )',
    'account number': -1,
    'group': 'N/A',
    'active': False,
}

DEFAULT_PROJECT_METADATA = {
    'CoreFacilityRef': 2,
    'ProjectName': '( Not found )',
    'Phase': -1,
    'Active': False,
    'BCode': -1,
    'ProjectRef': -1,
    'Affiliation': 'N/A',
    'ProjectType': 'N/A',
    'ProjectGroup': 'N/A',
}

@dataclass
class UserResult:
    metadata: dict = field(default_factory=lambda: DEFAULT_USER_METADATA)
    state: UserState = UserState()

    def to_dict(self):
        return {
            'metadata': self.metadata,
            'indicators': self.state.as_indicators(),
            'indicator_labels': self.state.get_header_list()            
        }

@dataclass
class ProjectResult:
    metadata: dict = field(default_factory=lambda: DEFAULT_PROJECT_METADATA)
    state: ProjectState = ProjectState()  

    def to_dict(self):
        return {
            'metadata': self.metadata,
            'indicators': self.state.as_indicators(),
            'indicator_labels': self.state.get_header_list()            
        }

def user_from_email(email: str):
    """
    get login associated with email

    """
    
    result = { 'login': '' }

    try:
        result = gather.user_details_by_email(email)

    finally:
        return result


def admin_status(login: str):
    """
    checks admin status

    downstream call a bit questionable:
        checking for rights on specific system via old API 
        will return optional "ADM" field if user is an admin
    """

    sysid = 1   #nominal system, happens to be the FIB

    result = { 'admin': False }

    try:
        _returned = rims.rightcheck(login, sysid)
        print(f"{_returned}")

        if _returned['admin'] == True:
            result['admin'] = True

    finally:
        return result


def populate_userdropdown():
    """
    generate a list of dicts for user logins and names for dash dropdown
    """
    uid_list, name_list = gather.gather_userlists()

    name_list, uid_list = utils.sort_paired(name_list, uid_list)

    options=[]

    for i, uid in enumerate(uid_list):
        options.append({'search': f"{name_list[i]} ({uid_list[i]})", 'login': uid_list[i], 'name': name_list[i]})
    
    return options


def get_default_user_indicator():
    user_result = UserResult()

    result = user_result.to_dict()

    return result

"""
def get_default_project_indicators():
    result = []

    project_result = ProjectResult()

    result.append(project_result.to_dict())

    return result
"""

def get_default_project_indicator():

    project_result = ProjectResult()

    result = project_result.to_dict()

    return result


def get_user_indicators(user_login):
    """
    compile dashboard state for this user
    """

    #data gathering
    #------------------
    user_dict = gather.get_user_details(user_login)

    user_rights = gather.get_user_rights_dict(user_login)

    #preprocessing
    #user_name = user_dict['name']
    #user_name_clean = utils.cleanup_user_name(user_name)
    #user_name_first_last = utils.reorder_user_name(user_name_clean)


    #user state
    #------------------
    user_state = logic.collate_user(user_rights)

    #FUTURE: save user_result to DB here

    user_result = UserResult(user_dict, user_state)

    result_dict = user_result.to_dict()

    print(f"returned userstate for user: {user_login}")

    return result_dict

def get_all_project_states():
    project_dicts = gather.get_projects_dict()

    result_dicts = []

    for item in project_dicts:
        project_state = logic.collate_project_dict(item)
        project_result = ProjectResult(item, project_state)
        result_dicts.append(project_result.to_dict())

    print(len(result_dicts))

    return result_dicts

def get_project_indicators(project_number):

    project_df = gather.gather_projectdetails(project_number)

    try:
        project_dict = project_df.to_dict('records')[0] #to-dict returns a list
        project_dict.pop('Descr', None) #remove description field
        project_state = logic.collate_project_dict(project_dict)        
        
        #FUTURE: save project_result to DB here        
                        
    except:
        #dict conversion will fail on inaccessible projects (eg. 1995)
        #return empty defaults for these
        project_state = ProjectState()
        project_dict = copy.deepcopy(DEFAULT_PROJECT_METADATA)

    project_result = ProjectResult(project_dict, project_state)

    return project_result


def get_user_project_indicators(user_login):

    #project state
    #------------------
    user_projects = rims.get_user_projects(user_login)

    project_results = []

    if not user_projects == [-1]:
        for project_number in user_projects:
        #try to find user name in project titles            
            project_result = get_project_indicators(project_number)
            project_results.append(project_result)
    else:
        #return empty array
        project_state = ProjectState()
        project_dict = copy.deepcopy(DEFAULT_PROJECT_METADATA)
        project_result = ProjectResult(project_dict, project_state)
        project_results.append(project_result)

    print(f"returned projectstates for user: {user_login}")

    #to dict for export
    result_dicts = []
    for project_result in project_results:
        result_dicts.append(project_result.to_dict())

    print(result_dicts)

    return result_dicts


def state_from_user(user_login):
    """
    compile dashboard state for this user
    """

    #data gathering
    #------------------
    user_dict = gather.get_user_details(user_login)

    user_rights = gather.get_user_rights_dict(user_login)

    #preprocessing
    #user_name = user_dict['name']
    #user_name_clean = utils.cleanup_user_name(user_name)
    #user_name_first_last = utils.reorder_user_name(user_name_clean)


    #user state
    #------------------
    user_state = logic.collate_user(user_rights)

    user_result = UserResult()
    user_result.metadata = user_dict
    user_result.state = user_state



    #project state
    #------------------
    user_projects = rims.get_user_projects(user_login)

    project_results = []

    if not user_projects == [-1]:
        for proj in user_projects:
        #try to find user name in project titles            
            project_df = gather.gather_projectdetails(proj)
            try:
                project_dict = project_df.to_dict('records')[0] #to-dict returns a list
                project_dict.pop('Descr', None) #remove description field
                project_state = logic.collate_project(project_df)                
            except:
                #dict conversion will fail on inaccessible projects (eg. 1995)
                #return empty defaults for these
                project_state = UserState()
                project_dict = copy.deepcopy(DEFAULT_PROJECT_METADATA)

            project_result = ProjectResult()
            project_result.metadata = project_dict
            project_state = project_state
            
            project_results.append(project_result.to_dict())
    else:
        #return empty array
        project_state = ProjectState()
        project_results.append(project_state.to_dict())


    #to-do:
    #   project.OHS using user_result and project_result
    #   loop through multiple projects

    #dict
    result = { 'user_result': user_result.to_dict(), 'project_results': project_results }

    print(f"result: {result}")

    return result
    #TODO test cases:
    #   ok project
    #   no projects
    #   ghost project (ie. 1995)
    #   only ghost project
    #   only bad projects
    #   CHECK alafif failing

