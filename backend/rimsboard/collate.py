import copy

from enum import Enum
from flask import jsonify
from dataclasses import dataclass, asdict, field


import rimsboard.rims as rims
import rimsboard.utils as utils
import rimsboard.usergather as gather

import rimsboard.logic as logic
from rimsboard.statelogic import Istate, UserState, UserStateLabels, ProjectState, ProjectStateLabels

DEFAULT_USER_METADATA = {}

DEFAULT_PROJECT_METADATA = {
    'CoreFacilityRef': 2,
    'ProjectName': '( Not found )',
    'Phase': '',
    'Active': '',
    'BCode': '',
    'ProjectRef': -1,
    'Affiliation': '',
    'ProjectType': '',
    'ProjectGroup': '',
}

@dataclass
class UserResult:
    metadata: dict = field(default_factory=lambda: DEFAULT_USER_METADATA)
    state: UserState = UserState()
    state_labels: dict = field(default_factory=lambda: {i.name: i.value for i in UserStateLabels})

    def to_dict(self):
        return {
            'metadata': self.metadata,
            'state_labels': self.labels,            
            'state': asdict(self.state),
        }

@dataclass
class ProjectResult:
    metadata: dict = field(default_factory=lambda: DEFAULT_PROJECT_METADATA)
    state: ProjectState = ProjectState()
    state_labels: dict = field(default_factory=lambda: {i.name: i.value for i in ProjectStateLabels})    


    def to_dict(self):
        return {
            'metadata': self.metadata,
            'state_labels': self.labels,
            'state': asdict(self.state),
        }


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



def get_user_state(user_login):
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

    print(f"returned userstate for user: {user_login}")

    return user_result



def get_user_project_states(user_login):

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
            
            project_results.append(project_result)
    else:
        #return empty array
        project_state = ProjectState()
        project_results.append(project_state)

    print(f"returned projectstates for user: {user_login}")

    return project_results


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

