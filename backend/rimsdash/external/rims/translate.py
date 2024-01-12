import re 
import logging
import json
from datetime import datetime

import rimsdash.config as config
import rimsdash.schemas as schemas

from .clean import strip_brackets, fix_special_chars
from rimsdash.models import SystemRight, ProjectRight, IStatus

RIMS_DATE_FORMAT_1 = "%Y/%m/%d %H:%M:%S"
RIMS_DATE_FORMAT_2 = "%Y/%m/%d %H:%M"

CORE_NAME:str = config.get('ppms', 'core_name')

logger = logging.getLogger('rimsdash')


def parse_rims_date(rims_date: str):
    """
    RIMS dates seem to use a variety of different formats

    Try them in sequence and return the first that is successful
    """
    try:
        result = datetime.strptime(rims_date, RIMS_DATE_FORMAT_1)
    except:
        try:
            result = datetime.strptime(rims_date, RIMS_DATE_FORMAT_2)
        except:
            result = datetime(2018, 1, 1)
            logging.error(f"WARNING: unable to parse date string {rims_date}, using 01/01/2018 instead")
    finally:
        return result

def validate_training_requests(rims_request_data: list[dict]) -> list[dict]:
    """
    validate return from system list report 
        against system schema
    """
    result = []

    for request in rims_request_data:

        schema = schemas.TrainingRequestReceiveSchema(
            id = request["reqId"],
            date = parse_rims_date(request["reqDate"]),
            new = request["reqNew"],
            type = request["reqType"],
            form_id = request["formId"],
            form_name = request["formName"],
            user_id = request["userId"],
        )

        result.append(schema.dict())
    
    return result

def validate_systems(rims_system_data: list[dict]) -> list[dict]:
    """
    validate return from system list report 
        against system schema
    """
    result = []

    for system in rims_system_data:

        _schema = schemas.SystemCreateSchema(
            id = system["id"], 
            system_type = system["type"], 
            name = system["name"]
        )

        result.append(_schema.to_dict())
    
    return result


def validate_user_list(rims_user_list: list[dict]) -> list[dict]:
    """
    validate return from user list report 
        against user schema
    """
    result = []

    for user in rims_user_list:

        _schema = schemas.UserCreateSchema(
            username = user['login'], 
            userid = user['id'], 
            name = strip_brackets(user['name']),
            email = user['email'],
            group = user['group'],
            active = user['active'],
        )

        result.append(_schema.to_dict())
    
    return result


def validate_project_list(rims_project_list: list[dict]) -> list[dict]:
    """
    validate return from project list report 
        against project schema
    """
    result = []

    for project in rims_project_list:

        _schema = schemas.project_schema.ProjectListTranslateSchema(
            id = project['ProjectRef'],
            title = fix_special_chars(project['ProjectName']),
            phase = project['Phase'],
            active = project['Active'],
            bcode = project['Bcode'],
            affiliation = project['Affiliation'],
            type = project['ProjectType'],
            group = project['ProjectGroup'],
            core_id = project['CoreFacilityRef'],
            description = fix_special_chars(project['Descr']),
        )

        result.append(_schema.to_dict())
    
    return result


def validate_admin_check(rights_dict: dict) -> bool:
    """
    validate admin status API return
    """
    result = False

    try:
        if rights_dict['rights']=='OK' and rights_dict['admin']==True:
            result = True
    
        _schema = schemas.user_schema.UserUpdateAdminSchema(admin=result)

    except:
        return False
    
    finally:
        return result

def validate_project_details(rims_project_details: list[dict]) -> list[dict]:
    """
    validate return from projectdetailsv2 report 
        against project schema
    
    NB: API currently returns all facilities, need to filter by core name
        this field really only appears in this report
    """

    result = []

    for project in rims_project_details:

        if CORE_NAME in project['Visibility'][:10]:

            _schema = schemas.ProjectInitDetailsSchema(
                id = project['Project ID'],
                qcollection = project['UQRDM Collection #'],
                status = project['Status'],
            )

            result.append(_schema.to_dict())
        else:
            pass
    
    return result
    """
    'Project ID': ,
    'Title': "",
    'Project type': '',
    'Main group': '',
    'Email of the supervisor': '',
    'Project requested by user name': '',
    'Project requested by user email': '',
    'Participant Users': '',
    'Participant Groups': ' ',
    'Visibility': '',
    'Account number': '',
    'Email of budget holder': '',
    'Expiration date': '',
    'Affiliation': '',
    'Phase': ,
    'Status': '',
    'Active': ,
    'Edu person principal name': '',
    'Sub org unit': '',
    'UQRDM Collection #': ''},
    """


def rims_link_extract_key(input: str, prefix: str) -> str:
    """
    get the key from a RIMS report hyperlink, by prefix
    """
    # Use a regular expression to match the pattern
    pattern = f"{prefix}=([^\]]+)"
    match = re.search(pattern, input)
    if match:
        return match.group(1)
    else:
        return ''    
    
def rims_link_extract_value(input: str) -> str:
    """
    get the value from a RIMS report hyperlink 
    """
    match = re.search(r"\(([^)]+)\)", input)
    if match:
        return match.group(1)
    else:
        return ''


def validate_account_list(rims_account_data: list[dict]) -> list[dict]:
    """
    validate return from #56 accounts report 

    NB: this is a complex join table, need to validate elements against account, project and projectaccount
    """

    result = []

    for acc in rims_account_data:

        #read the validity field and get as bool
        __valid = acc['Project Account Valid'] == 'YES'

        __valid

        #validate the project info
        #   skip if failed
        #   warn if failed on valid projaccount
        try:
            __project_schema = schemas.project_schema.ProjectFromAccountSchema(
                id = acc['Project ID'],
                title = rims_link_extract_value(acc['Project Name']),
                active = acc['Project Active'] == 'Active',
                group = acc['Group PI']
            )
            project_dict = __project_schema.dict()

        except:
            if __valid:
                logger.warn(f"project read failed for valid projaccount {acc['Project ID']}, {acc['Project Account']}, {acc['Group PI']}")
            continue
    
        #validate the account info  
        try:
            __account_schema = schemas.account_schema.AccountReceiveSchema(
                bcode = rims_link_extract_key(acc['Project Account'], 'bcode'),
            )
            account_dict = __account_schema.dict()

        except:
            if __valid:
                logger.warn(f"account read failed for valid projaccount {acc['Project ID']}, {acc['Project Account']}, {acc['Group PI']}")
            continue

        if account_dict['bcode'] == '' or account_dict['bcode'] is None:
            logger.warn(f"bcode empty for {acc['Project ID']}, {acc['Project Account']}, {acc['Group PI']}")
            continue

        #validate the join and validity
        __join_schema = schemas.projectaccount_schema.ProjectAccountReceiveSchema(
            bcode = account_dict['bcode'],
            project_id = project_dict['id'],
            valid = __valid,
        )
        projectaccount = __join_schema.dict()

        #drop the original primary keys to avoid duplicates
        del project_dict['id']
        del account_dict['bcode']

        #merge in the account and project dicts
        projectaccount.update(project_dict)
        projectaccount.update(account_dict) #NB currently empty as only contained bcode
        
        result.append(projectaccount)

    return result



def validate_user_rights_list(rims_rights_list: list[dict]) -> list[dict]:
    """
    validate return from user rights report 
        against user schema
    """
    result = []

    for user in rims_rights_list:

        __username = user['username']
        __rights_list = json.loads(user['Data'])

        for right in __rights_list:
            __system_id = right['SystemID']
            __status = SystemRight(right['Rights'])

            try:
                __schema = schemas.systemuser_schema.SystemUserReceiveSchema(
                    username=__username, 
                    system_id=__system_id, 
                    status=__status
                )
                result.append(__schema.dict())
            except:
                logger.info(f"error translating userright: {user['username']}, {right['SystemID']}")

    return result


def validate_user_projects_list(rims_projectrights_list: list[dict]) -> list[dict]:
    """
    validate return from user rights report 
        against user schema
    """
    result = []

    for project in rims_projectrights_list:

        __username = project['Username']
        __project_ids = json.loads(project['UserProjects'])

        for id in __project_ids:
            __project_id = id
            __status = ProjectRight('M')

            try:
                __schema = schemas.projectusers_schema.ProjectUsersReceiveSchema(
                    username=__username, 
                    project_id=__project_id, 
                    status=__status
                )
                result.append(__schema.dict())
            except:
                logger.info(f"error translating project right: {project['Username']}, {id}")

    return result