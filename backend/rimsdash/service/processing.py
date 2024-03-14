import logging
import datetime

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi_utils.session import FastAPISessionMaker

import rimsdash.config as config
import rimsdash.db as rdb
import rimsdash.external.rims as rims
import rimsdash.schemas as schemas
import rimsdash.crud as crud
import rimsdash.service.logic as logic

from rimsdash.models import SystemRight, ProjectRight, SyncType

logger = logging.getLogger('rimsdash')

#sessionmaker = FastAPISessionMaker(SQLALCHEMY_DATABASE_URL)

ACCEPTED_REALMS = {'admin', 'dashboard'}

def lookup_keycloak_user_access(db: Session, keycloak_user: dict) -> bool:
    """
    extracts user from decoded keycloak token and checks their access

    DEPRECATED
    """
    try:
        email = keycloak_user.get('email')
        realm_access = keycloak_user.get('realm_access')
    except:
        raise Exception(f"Error parsing keycloak user from token")

    #if the keycloak token has the appropriate realm (eg. admin), return ok
    if realm_access and \
        any ( realm in ACCEPTED_REALMS for realm in realm_access.get('roles') ):
        return True
    else:
        #otherwise look up the user and return their admin status for the dashboard core
        user = crud.user.get_by_email(db, email)
        
        if not email or not user:
            raise Exception(f"Non-admin user from keycloak token not found in DB for {email}, access denied")
        else:
            return user.admin

def log_sync_error(label, id):
    """
    logs an error during syncing
    handles the case that the id itself does not exist
    """
    try:
        logger.error(f"Failure syncing {label} at id: {id}")
    except:
        logger.error(f"Failure syncing item, id/label missing")


def sync_systems(db: Session = Depends(rdb.get_db)):
    """
    Sync local systems DB to external RIMS DB

    external data will overwrite any local conflicts
    """

    logger.info(f"getting system list from RIMS")
    systems: list[dict] = rims.get_system_list()

    logger.info(f"reading system list into DB")
    for system in systems:
        try:
            __row = crud.system.get(db, system['id'])

            if __row is None:
                logger.debug(f"creating system {system['id']}")
                system_in = schemas.SystemCreateSchema(**system)

                crud.system.create(db, system_in)
            else:
                logger.debug(f"updating system {system['id']}")            
                system_in = schemas.SystemCreateSchema(**system)

                crud.system.update(db, __row, system_in)
        except:
            log_sync_error("system", system['id'])

def sync_users(db: Session = Depends(rdb.get_db)):
    """
    Sync local user DB to external RIMS DB

    external data will overwrite any local conflicts
    """

    logger.info(f"getting user list from RIMS")
    users: list[dict] = rims.get_user_list()

    logger.info(f"reading user list into DB")
    for user in users:
        try:
            __row = crud.user.get(db, user['username'])

            if __row is None:
                logger.debug(f"creating user {user['username']}")
                user_in = schemas.UserCreateSchema(**user)

                crud.user.create(db, user_in)
            else:
                logger.debug(f"updating user {user['username']}")            
                user_in = schemas.UserUpdateSchema(**user)

                crud.user.update(db, __row, user_in)
        except:
            log_sync_error("user", user['username'])

def sync_user_admin(db: Session = Depends(rdb.get_db), skip_existing: bool = False):
    """
    Sync admin status in DB to external RIMS DB
    """
    logger.info(f"Syncing admin status")
    for __row in crud.user.get_all(db):
        try:
            if __row is not None:
                if skip_existing and __row.admin == False:
                    logger.debug(f"admin sync: SKIP {__row.username}")
                else:
                    logger.debug(f"admin sync: {__row.username}")
                    admin_dict = rims.get_admin_status(__row.username)

                    user_admin_in = schemas.user_schema.UserUpdateAdminSchema(**admin_dict)

                    crud.user.update(db, __row, user_admin_in)
        except:
            log_sync_error("user admin status", __row.username)

    
def sync_accounts(db: Session = Depends(rdb.get_db)) -> list[dict]:
    """
    Sync local account DB to external RIMS DB
    
    Update projects to include account

    external data will overwrite any local conflicts
    """

    logger.info(f"getting account list from RIMS")

    projectaccount_list: list[dict] = rims.get_project_accounts()

    logger.info(f"reading account list into DB")

    for acc in projectaccount_list:
        try:
            #now setup the account
            __row = crud.account.get(db, acc['bcode'])

            if __row is None:
                logger.debug(f"creating account {acc['bcode']}")
                account_in = schemas.AccountReceiveSchema(
                    bcode = acc['bcode'],
                )

                crud.account.create(db, account_in)
            else:
                logger.debug(f"updating account {acc['bcode']}")

                account_in = schemas.AccountReceiveSchema(
                    bcode = acc['bcode'],
                )
                crud.account.update(db, __row, account_in)
        except:
            log_sync_error("account", acc['bcode'])
    return projectaccount_list



def sync_projects(db: Session = Depends(rdb.get_db)):
    """
    Sync local project DB to external RIMS DB

    external data will overwrite any local conflicts
    """

    logger.info(f"getting project list from RIMS")
    projects: list[dict] = rims.get_project_list()

    logger.info(f"reading project list into DB")
    for project in projects:
        try:
            _row = crud.project.get(db, project['id'])

            if _row is None:
                logger.debug(f"creating project {project['id']}")
                project_in = schemas.ProjectCreateSchema(**project)

                crud.project.create(db, project_in)
            else:
                logger.debug(f"updating project {project['id']}")            
                project_in = schemas.ProjectCreateSchema(**project)

                crud.project.update(db, _row, project_in)
        except:
            log_sync_error("project", project['id'])

    logger.info(f"getting additional project details from RIMS")
    project_details: list[dict] = rims.get_project_details()

    logger.info(f"updating DB with additional project details")
    for project in project_details:
        try:
            _row = crud.project.get(db, project['id'])

            if _row is None:
                logger.warn(f"Project {project['id']} found in RIMS details report but not present in DB. Project ignored.")
                pass
            else:
                logger.debug(f"Updating project {project['id']}")   
                project_in = schemas.ProjectInitDetailsSchema(**project)

                crud.project.update(db, _row, project_in)
        except:
            log_sync_error("project", project['id'])
    return projects



def sync_training_request_forms(training_requests):
    pass





def sync_training_requests(db: Session = Depends(rdb.get_db)):
    """
    Sync local request DB to external RIMS DB

    external data will overwrite any local conflicts
    """

    logger.info(f"getting training requests from RIMS")
    training_requests: list[dict] = rims.get_training_request_list()

    logger.info(f"reading request list into DB")

    for trequest in training_requests:
        try:
            #use the RIMS uid to get a username
            __user = crud.user.get_by_userid(db, userid=trequest['user_id'])

            if __user is not None:
                trequest['username'] = __user.username

                __row = crud.trequest.get(db, trequest['id'])

                if __row is None:
                    logger.debug(f"creating request {trequest['id']} for user {trequest['username']}")

                    trequest_in = schemas.TrainingRequestCreateSchema.parse_obj(trequest)

                    crud.trequest.create(db, trequest_in)
                else:
                    logger.debug(f"updating request {trequest['id']} for user {trequest['username']}")

                    trequest_in = schemas.TrainingRequestCreateSchema.parse_obj(trequest)

                    crud.trequest.update(db, __row, trequest_in)
            else:
                logger.warn(f"RIMS uid {trequest['user_id']} from training request  {trequest['id']} not found in local DB")
        except:
            log_sync_error("trequest", trequest['user_id'])

    #FUTURE
    #get list of unique form ids from database
    __form_ids = config.get_csv_list("manual", "training_form_ids", default = [])
    form_ids = list(map(int, __form_ids))

    for form_id in form_ids:
        trequest_forms_for_id: list[dict] = rims.get_trequest_content_list(form_id)

        for trform in trequest_forms_for_id:
            try:
                row = crud.trequest.get(db, trform['id'])

                if row is None:
                    logger.error(f"request {trform['id']} for user {trform['user_fullname']} not found in DB")
                    pass
                else:

                    logger.debug(f"adding form data to {trform['id']} for user {row.username}")

                    trequest_in = schemas.TrainingRequestAddFormDataSchema.parse_obj(trform)

                    crud.trequest.update(db, row, trequest_in)
            except:
                log_sync_error("trform", trform['id'])        

def match_project_account_pair(projectaccount_list: list[dict], bcode: str, project_id: int) -> dict:
    """
    find the corresponding project-account pair in a rims projacc list
    
    does not check for duplicates    
    """

    for __projacc in projectaccount_list:
        if __projacc['bcode'] == bcode and __projacc['project_id'] == project_id:
            return __projacc     

    #if not found, warn and return the ids with valid = None
    logger.warn(f"pair | pid: {project_id} | bcode: {bcode} | not found in RIMS project-account report, setting valid = None")    
    return { 'bcode': bcode, 'project_id': project_id, 'valid': None }



def sync_project_accounts(project_list: list[dict], projectaccount_list: list[dict], db: Session = Depends(rdb.get_db)):
    """
    Sync project-account pairs to DB

    Iterates through rims-projects and matches to rims-projectaccounts via DB
    """

    logger.info(f"creating projacc")

    #projectaccount_list: list[dict] = rims.get_project_accounts()

    for project in project_list:
        try:
            #warn and skip if the account does not exist
            if project['bcode'] == '':
                logger.warn(f"empty bcode {project['bcode']} for project {project['id']}")   

            #if the account is in the DB, find the pair from the local list
            if crud.account.get(db, project['bcode']) is not None:
                project_account = match_project_account_pair(projectaccount_list, project['bcode'], project['id'])
            else:           
                #if the account is not in the DB, create it with valid = None 
                logger.warn(f"account {project['bcode']} not found in DB for project {project['id']}, creating w/ valid=None")
                __account_schema = schemas.account_schema.AccountCreateSchema(
                    bcode = project['bcode']
                )
                crud.account.create(db, __account_schema)
                project_account = { 'bcode': project['bcode'], 'project_id': project['id'], 'valid': None }

            #link the project and account
            projacc_in = schemas.ProjectAccountReceiveSchema(
                bcode = project['bcode'],
                project_id = project['id'],
                valid = project_account['valid'],
            )

            __row = crud.projectaccount.get(db, (project['bcode'], project['id']) )

            if __row is None:
                crud.projectaccount.create(db, projacc_in)
            else:
                crud.projectaccount.update(db, __row, projacc_in)
        except:
            log_sync_error("project", project['id'])               


def update_accounts(projectaccount_list, projects, db: Session = Depends(rdb.get_db)):
    """
    DEPRECATED
    """

    logger.info(f"reading account list into DB")

    #projectaccount_list: list[dict] = rims.get_project_accounts()

    for acc in projectaccount_list:
        #first, confirm the project exists
        __proj = crud.project.get(acc['project_id'])

        if __proj is None:
            logger.warn(f"project {acc['project_id']} not found in DB for account {acc['bcode']} - skipping")
            continue
        
        #next, link the project and account
        projacc_in = schemas.ProjectAccountReceiveSchema(
            bcode = acc['bcode'],
            project_id = acc['project_id'],
            valid = acc['valid'],
        )

        __row = crud.projectaccount.get(db, (acc['bcode'], acc['project_id']) )

        if __row is None:
            crud.projectaccount.create(db, projacc_in)
        else:
            crud.projectaccount.update(db, __row, projacc_in)



def sync_user_rights(db: Session = Depends(rdb.get_db)):
    """
    Sync local user rights DB to external RIMS DB

    external data will overwrite any local conflicts
    """

    logger.info(f"Getting user rights from RIMS")

    user_rights_list = rims.get_user_rights_list()

    for user_right in user_rights_list:

        try:
            logger.debug(f"user right for {user_right['username']}")

            #check both system and user exist
            user = crud.user.get(db, user_right['username'])
            if user is None:
                logger.info(f"unrecognised user {user_right['username']} in rims user_rights_list")                     
                continue              

            system = crud.system.get(db, user_right['system_id'])
            if system is None:
                logger.info(f"unrecognised system {user_right['system_id']} for user {user_right['username']}")                     
                continue  

            __schema = schemas.SystemUserCreateSchema(**user_right)
            __row = crud.systemuser.get(db, (__schema.username, __schema.system_id))

            if __row is None:
                crud.systemuser.create(db, __schema)
            else:
                crud.systemuser.update(db, __row, __schema)
        except:
            log_sync_error("user_right", user_right['username'])


def sync_user_rights_indiv(db: Session = Depends(rdb.get_db)):
    """
    Sync local user rights DB to external RIMS DB

    external data will overwrite any local conflicts

    DEPRECATED - many calls to external API
    """
    
    logger.info(f"Getting individual user rights from RIMS")

    users = crud.user.get_all(db)
    
    #DEBUG
    _cutoff = 99999
    _counter = 0

    for user in users:
        if _counter >= _cutoff: #debug
            break

        logger.debug(f"sync rights {user.username}")
        rights_dict = rims.queries.get_user_rights(user.username)

        for key in rights_dict:
            __schema = schemas.SystemUserCreateSchema(username=user.username, system_id=key, status=SystemRight(rights_dict[key]))

            __row = crud.systemuser.get(db, (user.username, key))
            __system = crud.system.get(db, key)

            #check system exists - report includes systems from other cores            
            if __system is not None:

                if __row is None:
                    crud.systemuser.create(db, __schema)
                else:
                    crud.systemuser.update(db, __row, __schema)
            else:
                logger.debug(f"unrecognised rights for user {user.username} on system {key}")    
        
        _counter+=1 #debug



def sync_project_users(db: Session = Depends(rdb.get_db)):
    """
    Sync local project membership DB to external RIMS DB

    external data will overwrite any local conflicts
    """

    logger.info(f"Syncing project rights to RIMS")

    user_projects_list = rims.get_user_projects_list()

    for project_user in user_projects_list:
        try:
            logger.debug(f"project membership for {project_user['username']}")

            #check both user and project exist
            user = crud.user.get(db, project_user['username'])
            if user is None:
                logger.info(f"unrecognised user {project_user['username']} in rims user_projects_list")                     
                continue

            project = crud.project.get(db, project_user['project_id'])
            if project is None:
                logger.info(f"unrecognised system {project_user['project_id']} for user {project_user['username']}")                     
                continue

            __schema = schemas.ProjectUsersReceiveSchema(**project_user)
            __row = crud.projectuser.get(db, (__schema.username, __schema.project_id))

            if __row is None:
                crud.projectuser.create(db, __schema)
            else:
                crud.projectuser.update(db, __row, __schema)
        except:
            log_sync_error("project_user", project_user['username'])

def sync_project_users_indiv(db: Session = Depends(rdb.get_db)):
    """
    Sync local project users DB to external RIMS DB

    external data will overwrite any local conflicts

    DEPRECATED - many calls to external API
    """
    
    logger.info(f"syncing project users to RIMS")

    projects = crud.project.get_all(db)

    #DEBUG
    _cutoff = 99999
    _counter = 0

    for project in projects:
        if _counter >= _cutoff: #debug
            break

        logger.debug(f"sync project users {project.id}")
        username_list = rims.queries.get_project_users(project.id)

        for username in username_list:
            __schema = schemas.ProjectUsersBaseSchema(username=username, project_id=project.id, status=ProjectRight("M"))

            __row = crud.projectuser.get(db, (username, project.id))

            if __row is None:
                crud.projectuser.create(db, __schema)
            else:
                crud.projectuser.update(db, __row, __schema)
 
        _counter+=1 #debug

def process_projects(db: Session = Depends(rdb.get_db)):
    """
    Calculate status for projects
    """

    projects = crud.project.get_all(db)

    for project in projects:
        try:
            logger.debug(f"project state: {project.id}")
            project_schema = schemas.ProjectForStateCheckSchema.from_orm(project)

            project_state = logic.process_project(project_schema)

            _row = crud.project_state.get(db, project.id)

            #FUTURE: need to sort out create vs update, much simpler if can unify
            if _row is None:
                project_state = schemas.ProjectStateCreateSchema.validate(project_state)
                crud.project_state.create(db, project_state)
            else:
                project_state = schemas.ProjectStateUpdateSchema.validate(project_state)
                crud.project_state.update(db, _row, project_state)
        except:
            log_sync_error("project state", project.id)

def process_users(db: Session = Depends(rdb.get_db)):
    """
    calculate status for users
    """
    users = crud.user.get_all(db)

    for user in users:
        try:
            logger.debug(f"user state: {user.username}")
            user_schema = schemas.UserForStateCheckSchema.from_orm(user)

            user_state = logic.process_user(user_schema)

            _row = crud.user_state.get(db, user.username)

            #FUTURE: need to sort out create vs update, much simpler if can unify
            if _row is None:
                user_state = schemas.UserStateCreateSchema.validate(user_state)
                crud.user_state.create(db, user_state)
            else:
                user_state = schemas.UserStateUpdateSchema.validate(user_state)
                crud.user_state.update(db, _row, user_state)
        except:
            log_sync_error("user state", user.username)

def postprocess_projects(db: Session = Depends(rdb.get_db)):
    
    projects = crud.project.get_all(db)

    for project in projects:
        try:
            logger.debug(f'posprocessing proj {project.id}')
            project_schema = schemas.ProjectOutRefsSchema.from_orm(project)

            project_state_updated = logic.postprocess_project(project_schema)

            _row = crud.project_state.get(db, project.id)

            if _row is not None:
                project_state = schemas.ProjectStatePostProcessUpdateSchema.validate(project_state_updated)
                crud.project_state.update(db, _row, project_state)
            else:
                logger.warn(f'project-state {project.id} not found in database after update')
        except:
            log_sync_error("project post-state", project.id)

def postprocess_users(db: Session = Depends(rdb.get_db)):
    
    users = crud.user.get_all(db)

    for user in users:
        try:
            logger.debug(f'posprocessing user {user.username}')
            user_schema = schemas.UserOutRefsSchema.from_orm(user)

            user_state_updated = logic.postprocess_user(user_schema)

            _row = crud.user_state.get(db, user.username)

            if _row is not None:
                user_state = schemas.UserStatePostProcessUpdateSchema.validate(user_state_updated)
                crud.project_state.update(db, _row, user_state)
            else:
                logger.warn(f'user-state {user.username} not found in database after update')
        except:
            log_sync_error("user post-state", user.username)

def process_trequests(db: Session = Depends(rdb.get_db)):
    
    trequests = crud.trequest.get_all(db)

    for trequest in trequests:
        try:
            logger.debug(f'posprocessing training request  {trequest.id}')
            trequest_schema = schemas.TrainingRequestForProcessingSchema.from_orm(trequest)

            trequest_updated: schemas.TrainingRequestUpdateStateSchema \
                = logic.process_trequest(trequest_schema)

            _row = crud.trequest.get(db, trequest.id)

            if _row is not None:
                crud.trequest.update(db, _row, trequest_updated)
            else:
                logger.warn(f'training request {trequest.id} absent in DB on attempted update')
        except:
            log_sync_error("trequest state", trequest.id)


def rims_sync_batch_lists(db):
    """
    sync batchable report data only

    NB: fairly quick
    """    
    logger.info(">>>>>>>>>>>> Begin syncing batch data from RIMS")
    sync_systems(db)
    sync_users(db)

    #   FUTURE refactor these 
    project_list = sync_projects(db)
    projectaccount_list = sync_accounts(db)
    sync_project_accounts(project_list, projectaccount_list, db)
    #   /end refactor target

    sync_user_rights(db)
    sync_project_users(db)
    sync_training_requests(db)

    logger.info(">>>>>>>>>>>> Finished syncing batch data from RIMS")


def rims_sync_individual(db):
    """
    sync additional data requiring individual calls

    NB: slow!
    """
    logger.info(">>>>>>>>>>>> Begin syncing individual data from RIMS")
    sync_user_admin(db, skip_existing = True)
    logger.info(">>>>>>>>>>>> Finished syncing individual data from RIMS")


def calc_states(db):
    """
    recalculate states only
    """
    logger.info(">>>>>>>>>>>> Begin calculating states")
    process_projects(db)
    process_users(db)
    postprocess_projects(db)
    postprocess_users(db)
    process_trequests(db) 
    logger.info(">>>>>>>>>>>> Finished calculating states")

def dummy_sync(db):
    """
    add dummy sync to DB
    """
    logger.info(">>>>>>>>>>>> DEV adding fake sync to DB")
    #FUTURE: add a dummy sync type to models/base_model
    __start_schema = schemas.SyncCreateSchema(sync_type=SyncType.full)
    __current = crud.sync.create(db, __start_schema)

    __complete_schema = schemas.SyncCompleteSchema(id=__current.id, sync_type=__current.sync_type)
    __updated = crud.sync.update(db, __current, __complete_schema)

    __last = crud.sync.get_latest_completion(db)
    logger.info(">>>>>>>>>>>> DEV finished adding fake sync to DB")



def remake_db(db, force=False):
    if force == True:
        rdb.drop_db(force=True)

        rdb.init_db()    

        new_db = rdb.get_session()

    return new_db


def primary_sync(db: Session = Depends(rdb.get_db), force=False):
        """
        perform full sync

        WARNING: many RIMS API calls (6k+)
            to be reduced by new reports when available
        """

        if config.get('sync', 'recreate_db', default=True) == "True":
            remake = True
        else:
            remake = False

        if remake:
            logger.info("!!!!wipe and recreate DB")
            db = remake_db(db, force=remake)
        
        sync_frequency_days = int(config.get('sync', 'full_sync_frequency', default=1))

        try:
            __last = crud.sync.get_latest_completion(db)
        except:
            __last = None

                #FUTURE update the time delta here to allow sync at -5 min

        try:
            time_since_sync = datetime.datetime.now() - __last.start_time       
        except:
            time_since_sync = datetime.timedelta(seconds=1)
            
        delta = datetime.timedelta(days=sync_frequency_days) - datetime.timedelta(minutes=5)

        if force or __last is None or (time_since_sync  >= delta):
            logger.info(">>>>>>>>>>>> Begin full sync")
            __start_schema = schemas.sync_schema.SyncCreateSchema(sync_type=SyncType.full)
            __current = crud.sync.create(db, __start_schema)

            try:
                rims_sync_batch_lists(db)

                if True:
                    rims_sync_individual(db)
                calc_states(db)

                __complete_schema = schemas.sync_schema.SyncCompleteSchema(id=__current.id, sync_type=__current.sync_type)
                __updated = crud.sync.update(db, __current, __complete_schema)
                logger.info(">>>>>>>>>>>> Completed full sync")
            except:
                logger.error("!!!!! ERROR: Sync not completed")
                __complete_schema = schemas.sync_schema.SyncCompleteSchema(id=__current.id, sync_type=__current.sync_type, complete=False)
                __updated = crud.sync.update(db, __current, __complete_schema)
        else:
            logger.warn(">>>>>>>>>>>> Sync not attempted, time difference less than sync frequency")


"""
managing accounts/projects is a bit complex

sync_accounts to populate just the accounts with bcodes

sync_projects to populate projects
    likely needs to look up accounts db to properly populate join table
    if projectaccount does not exist
        assign valid = False
    else:
        valid = row.valid

now update_accounts to assign validity to all project accounts
    any weirdness will show here, so maybe check consistency

"""

"""
FUTURE: refactor project_list, projectaccount_list to reduce passing of secondary lists above

pseudo:

#empty projectaccounts table?

def sync_projects                
    for project in projects
        if crud.account.get(db, bcode) is None:
            __aschema = schemas.xxx.(bcode = bcode)
            crud.account.create(db, __aschema)
        if crud.projectaccount.get(db, bcode, project_id) is None:
            __paschema = schemas.xxx.(..., valid = None)
            crud.projectaccount.create(db, __paschema)
    
palist = rims.getxxxx

def match_projectaccounts:
    for pa in palist:
        if crud.projectaccount.get(db, bcode, project_id):
            __paschema( valid = pa['valid'])
            crud.projectaccount.update(db, __paschema)

"""
