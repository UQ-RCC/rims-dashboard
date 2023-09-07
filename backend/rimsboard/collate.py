import copy

from enum import Enum
from flask import jsonify
from dataclasses import dataclass, asdict, field


import rimsboard.rims as rims
import rimsboard.utils as utils
import rimsboard.usergather as gather

from rimsboard.logic import ISTATES, IndicatorState, IndicatorStateGroup
from rimsboard.statelogic import Indicator

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




#NOTE: can't assign defaults here, maybe problem with custom classes
#   have to define these below in DEFAULT_*_STATE
@dataclass
class UserState:
    total: Indicator
    active: Indicator 
    access: list = field(default_factory=list)

    def to_list(self):
        #flatten to list

        result = [ asdict(self.total), asdict(self.active) ]

        #future: add check for non-unique keys
        for lab in self.access:
            result.append(asdict(lab))

        return result

@dataclass
class ProjectState:
    total: Indicator 
    active: Indicator 
    billing: Indicator 
    ohs: Indicator 
    rdm: Indicator 
    phase: Indicator      
    id: Indicator   #id only, used as wrapper for label value

    def to_list(self):
        result = [ asdict(self.total), asdict(self.active), asdict(self.billing), \
                  asdict(self.ohs), asdict(self.rdm), asdict(self.phase), asdict(self.id) ]

        return result

@dataclass
class ProjectStateList:
    projects: list = field(default_factory=list)

    def to_list(self):
            result = [ ]
            for proj in self.projects:
                result.append(proj.to_list())

            return result

#DEFAULTS

#rims codes for each lab & access-level
RIMS_LAB_CODES_PRIME = [ 82, 89, 87, -1]
RIMS_LAB_CODES_AH = [ 83, 88, 86, 84]
                #Ha, AIBN, Chem, QBP

#keys/labels for dataclasses - order must match list of rims codes above                
RIMS_LAB_KEYS = [ 'aibn', 'hawken', 'chem', 'qbp']
RIMS_LAB_LABELS = [ 'AIBN', 'Hawken', 'Chemistry', 'QBP']

#   copied from dataclasses above
#   hack due to custom classes not working as default in dataclass
#   used as base for derived states 
DEFAULT_USER_STATE = UserState( \
        total = Indicator("total", ISTATES.off, label="OK"), \
        active = Indicator("active", ISTATES.off, label="User account"), \
        access = [ 
            Indicator(RIMS_LAB_KEYS[0], ISTATES.off, label=RIMS_LAB_LABELS[0]),
            Indicator(RIMS_LAB_KEYS[1], ISTATES.off, label=RIMS_LAB_LABELS[1]),
            Indicator(RIMS_LAB_KEYS[2], ISTATES.off, label=RIMS_LAB_LABELS[2]),
            Indicator(RIMS_LAB_KEYS[3], ISTATES.off, label=RIMS_LAB_LABELS[3]),
        ]
)

DEFAULT_PROJECT_STATE = ProjectState( \
        total = Indicator("total", ISTATES.off, label="OK"), \
        active = Indicator("active", ISTATES.off, label="Active"), \
        billing = Indicator("financial", ISTATES.off, label="Billing"), \
        ohs = Indicator("ohs", ISTATES.off, label="OHS"), \
        rdm = Indicator("rdm", ISTATES.off, label="RDM"), \
        phase = Indicator("phase", ISTATES.off, label="Phase"),        
        id = Indicator("id", ISTATES.off, label="N/A")
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

    #data gathering
    #------------------
    user_dict = gather.get_user_details(user_login)

    user_projects = rims.get_user_projects(user_login)
    
    rights_df = gather.get_user_rights_df(user_login)

    #user state
    #------------------
    user_state = collate_user(rights_df)

    #project state
    #------------------

    #preprocessing
    user_name = user_dict['name']
    user_name_clean = utils.cleanup_user_name(user_name)
    user_name_first_last = utils.reorder_user_name(user_name_clean)

    oldest=None
    oldest_active=None
    found=False

    if not user_projects == [-1]:
        for proj in user_projects:
        #try to find user name in project titles            
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


        #generate the state for this project
        project_state = collate_project(project_df)
    else:
        #return empty array
        project_state = copy.deepcopy(DEFAULT_USER_STATE)

    #to-do:
    #   project.OHS using user_result and project_result
    #   loop through multiple projects

    project_states = ProjectStateList([ ])
    project_states.projects.append(project_state)

    #dict
    result = { 'user': user_state.to_list(), 'user_projects': project_states.to_list() }

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

    user_state = copy.deepcopy(DEFAULT_USER_STATE)

    if len(df) == 0:
        return user_state

    for i, code in enumerate(RIMS_LAB_CODES_PRIME):
        access_level = None
        row = df.loc[df['systemid'] == code]['access_level']

        try:
            access_level = row.iloc[0]

            if access_level in ['N', 'A', 'S']:
                user_state.access[i].state = ISTATES.ready
            elif access_level == 'D':
                user_state.access[i].state = ISTATES.disabled
            else:
                user_state.access[i].state = ISTATES.off
        
        except:
            print(f'unexpected access {access_level} for lab: {i}, {code}')
            user_state.access[i].state = ISTATES.na

    for i, code in enumerate(RIMS_LAB_CODES_AH):
        row = df.loc[df['systemid'] == code]['access_level']

        try:
            access_level = row.iloc[0]

            if access_level in ['N', 'A', 'S']:
                user_state.access[i].state = ISTATES.extended

        except:
            pass
    
    #TO-DO get this from df
    user_state.active.state = ISTATES.ready

    #calc overall from other states
    if user_state.active.state == ISTATES.ready and \
            all((lab.state == ISTATES.ready or lab.state == ISTATES.extended) for lab in user_state.access):

        user_state.total.state = ISTATES.ready
    else:
        user_state.total.state = ISTATES.off

    return user_state


def collate_project(df):
    
    project_state = copy.deepcopy(DEFAULT_PROJECT_STATE)

    try:
        if len(df) == 0:
            return project_state

        project_state.id.label = str(int(df['ProjectRef']))

        phase = df['Phase'].iloc[0]

        if phase == 0:
            project_state.phase.state = ISTATES.waiting
        elif phase == 1:
            project_state.phase.state = ISTATES.waiting
        elif phase == 2:
            project_state.phase.state = ISTATES.ready
        elif phase == 3:
            project_state.phase.state = ISTATES.disabled

        if bool(df['Active'].iloc[0]) == True:
            project_state.active.state = ISTATES.ready
        
        if not df['Bcode'].iloc[0] is None:
            project_state.billing.state = ISTATES.ready
            #future: check financial report for chartstring validity

        #if has rights in any lab
        #or is fee-for-service
        project_state.ohs.state = ISTATES.ready    #TO-DO

        #if has an RDM assigned
        project_state.rdm.state = ISTATES.ready    #TO-DO

        #set overall from other states
        all_ready = \
            project_state.active.state == ISTATES.ready and \
            project_state.billing.state == ISTATES.ready and \
            project_state.ohs.state == ISTATES.ready and \
            project_state.rdm.state == ISTATES.ready and \
            project_state.phase.state == ISTATES.ready and \
            project_state.id >= 0

        if all_ready:
            project_state.total.state = ISTATES.ready
        else:
            project_state.total.state = ISTATES.off

    finally:
        return project_state