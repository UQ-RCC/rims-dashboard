import logging

import rimsdash.schemas as schemas

from rimsdash.models import IStatus, UserStateModel, ProjectStateModel, SystemRight, AdminRight

from rimsdash.schemas import UserForStateCheckSchema, UserStateInitSchema, ProjectStateInitSchema, ProjectForStateCheckSchema, ProjectOutRefsSchema, ProjectStatePostProcessUpdateSchema, UserStatePostProcessUpdateSchema, UserOutRefsSchema


import rimsdash.config as config
import rimsdash.utils.utils as utils

logger = logging.getLogger('rimsdash')

EXTERNAL_AFFILIATIONS = config.get_csv_list('manual', 'external_affiliations', default = [])
UNLISTED_STAFF = config.get_csv_list('manual', 'unlisted_staff', default = [])

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


def process_user(user: UserForStateCheckSchema) -> UserStateInitSchema:
    """
    generate status result from user data
    """

    #initialise to labs not needed
    state = UserStateInitSchema(
        username=user.username,
        access_hawken=IStatus.off,        
        access_aibn=IStatus.off,
        access_chem=IStatus.off,
        access_qbp=IStatus.off,        
        access_pitschi=IStatus.incomplete,
    )

    try:
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
                    state.access_pitschi = IStatus.ready

        #admin pitschi cheat
        if user.admin == AdminRight.admin:
            state.access_pitschi = IStatus.ready

        if user.active == True:
            state.active = IStatus.ready
        else:
            state.active = IStatus.incomplete
        
        if state.active in [ IStatus.off, IStatus.ready ] and \
            state.access_pitschi in [ IStatus.off, IStatus.ready ] \
            and any(
                (labstate in [ IStatus.ready, IStatus.extended ] ) for \
                labstate in [ state.access_hawken, state.access_aibn, state.access_chem, state.access_qbp ]
        ):
            state.ok_user = IStatus.ready
        else:
            state.ok_user = IStatus.incomplete
    except:
        logger.error(f"error generating user state for {user.username}", exc_info=True)

    finally:
        return state



def process_project(project: ProjectForStateCheckSchema) -> ProjectStateInitSchema:
    """
    generate status result from project data
    """
    state = ProjectStateInitSchema(project_id = project.id)

    try:
        #phase
        if project.phase == 0:
            state.phase = IStatus.incomplete
        elif project.phase == 1:
            state.phase = IStatus.incomplete
        elif project.phase == 2:
            state.phase = IStatus.incomplete
        elif project.phase == 3:
            state.phase = IStatus.ready
        elif project.phase == 4:
            state.phase = IStatus.incomplete            
        else:
            state.phase = IStatus.incomplete

        #activity status
        if project.active == True:
            state.active = IStatus.ready
        else:
            state.active = IStatus.incomplete

        
        #billing
        if project.affiliation in EXTERNAL_AFFILIATIONS:
            state.billing = IStatus.ready
        else:
            try:                
                if project.project_account[0].valid == True:
                    state.billing = IStatus.ready
                elif project.project_account[0].valid == False:
                    state.billing = IStatus.incomplete
            except:
                state.billing = IStatus.incomplete                        
            

        #FUTURE: if has rights in any lab
        #or is fee-for-service
        state.ohs = state.phase    #TO-DO

        #if has an RDM assigned
        if project.qcollection is not None and not project.qcollection == '':
            state.rdm = IStatus.ready    
        else:
            state.rdm = IStatus.incomplete

        #set overall from other states
        all_ready = \
            state.active in [ IStatus.off, IStatus.ready ] and \
            state.billing in [ IStatus.off, IStatus.ready ] and \
            state.ohs in [ IStatus.off, IStatus.ready ] and \
            state.rdm in [ IStatus.off, IStatus.ready ] and \
            state.phase in [ IStatus.off, IStatus.ready ]

        if all_ready:
            state.ok_project = IStatus.ready
        else:
            state.ok_project = IStatus.incomplete
    except:
        logger.error(f"error generating project state for {project.id}", exc_info=True)

    finally:
        return state



def postprocess_project(project: ProjectOutRefsSchema) -> ProjectStatePostProcessUpdateSchema:
    
    project_state = ProjectStatePostProcessUpdateSchema(
            project_id = project.id, 
            ok_project = project.project_state.ok_project,             
            ok_user = IStatus.incomplete,
            ok_all = IStatus.incomplete,
        )

    try:

        admin_only_project = True

        #search for non-admin users
        #   if non-admin user is ok, project is user_ok
        for user_right in project.user_rights:
            
            if not ( user_right.user.admin == AdminRight.admin or user_right.user.admin == AdminRight.previous ):

                admin_only_project = False
                
                if user_right.user.user_state.ok_user == IStatus.ready:
                    project_state.ok_user = IStatus.ready

        if admin_only_project:
            project_state.ok_user = IStatus.ready
            
        if project.type == "Fee for Service":
            project_state.ok_user = IStatus.off

        if project_state.ok_project == IStatus.ready \
                and (project_state.ok_user in [ IStatus.off, IStatus.ready ] ):
            project_state.ok_all = IStatus.ready

    except:
        logger.error(f"error post-processing project state {project.id}", exc_info=True)
    
    finally:
        return project_state


def postprocess_user(user: UserOutRefsSchema) -> UserStatePostProcessUpdateSchema:
    
    user_state = UserStatePostProcessUpdateSchema(
        username = user.username, 
        ok_user = user.user_state.ok_user,
        ok_project = IStatus.incomplete,
        ok_all = IStatus.incomplete,
    )

    try:
        for project_right in user.project_rights:
            __project_state = project_right.project.project_state

            if __project_state.ok_project == IStatus.ready:
                user_state.ok_project = IStatus.ready
                break

        if user.admin == AdminRight.admin:
            user_state.ok_project = IStatus.off

        if user_state.ok_user == IStatus.ready \
                and (user_state.ok_project in [ IStatus.off, IStatus.ready ] ):
            user_state.ok_all = IStatus.ready

    except:
        logger.error(f"error post-processing user state {user.username}", exc_info=True)

    finally:
        return user_state


def process_trequest(trequest: schemas.TrainingRequestForProcessingSchema) -> schemas.TrainingRequestUpdateStateSchema:
    
    return_trequest = schemas.TrainingRequestUpdateStateSchema(id = trequest.id, state = IStatus.incomplete )

    try:
        user_state = trequest.user.user_state

        #good if user ok and has project that is ok, or is staff
        if ( user_state.ok_all == IStatus.ready ) or trequest.user.admin == AdminRight.admin:
            return_trequest.state = IStatus.ready

    except:
        logger.error(f"error generating trequest state for {trequest.id}", exc_info=True)

    finally:
        return return_trequest
