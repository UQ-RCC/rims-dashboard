import re 
import copy
import logging
import json
from datetime import datetime

import rimsdash.config as config
import rimsdash.schemas as schemas

from .clean import rims_strip_username_brackets, rims_substitute_notatinos
from .finalise import consolidate_duplicate_rights
from rimsdash.models import SystemRight, ProjectRight, IStatus, AdminRight

RIMS_DATE_FORMAT_1 = "%Y/%m/%d %H:%M:%S"
RIMS_DATE_FORMAT_2 = "%Y/%m/%d %H:%M"
RIMS_DATE_FORMAT_3 = "%Y/%m/%d"

CORE_NAME:str = config.get('ppms', 'core_name', required=True)
PREVIOUS_STAFF_USERNAMES:list = config.get_csv_list('manual','unlisted_staff')

logger = logging.getLogger('rimsdash')


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

def strip_brackets(input: str) -> str:
    """
    remove any content in brackets from a string 
    """    
    return re.sub(r'\(.*?\)', '', input).strip()

def write_rims_api_date(date: datetime):
    """
    RIMS API needs date in format year-month-day
    """
    return date.strftime('%Y-%m-%d')

def rims_form_get_final_line(input: str):
    """
    RIMS form questions print three whitespace chars at EOL

    Take final line from the input string to truncate question
    """    
    return input.rsplit('   ', 1)[-1]

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
            try:
                result = datetime.strptime(rims_date, RIMS_DATE_FORMAT_3)
            except:
                result = datetime(2018, 1, 1)
                logging.error(f"WARNING: unable to parse date string {rims_date}, using 01/01/2018 instead")
        
    finally:
        return result



def validate_systems(rims_system_data: list[dict]) -> list[dict]:
    """
    validate return from system list report 
        against system schema
    """
    result = []

    for system in rims_system_data:

        _schema = schemas.SystemReceiveSchema(
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

        _schema = schemas.UserReceiveSchema(
            username = user['login'], 
            userid = user['id'], 
            name = rims_strip_username_brackets(user['name']),
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
            title = rims_substitute_notatinos(project['ProjectName']),
            phase = project['Phase'],
            active = project['Active'],
            bcode = project['Bcode'],
            affiliation = project['Affiliation'],
            type = project['ProjectType'],
            group = project['ProjectGroup'],
            core_id = project['CoreFacilityRef'],
            description = rims_substitute_notatinos(project['Descr']),
        )

        result.append(_schema.to_dict())
    
    return result


def validate_admin_check(rights_dict: dict) -> dict:
    """
    validate admin status API return
    """

    #default to user
    result = schemas.user_schema.UserUpdateAdminSchema(
        admin=AdminRight.user
    )

    try:
        if rights_dict['rights']=='OK' and rights_dict['admin']==True:
            result = schemas.user_schema.UserUpdateAdminSchema(
                admin=AdminRight.admin
            )
            
        elif rights_dict['login'] in PREVIOUS_STAFF_USERNAMES:
            result = schemas.user_schema.UserUpdateAdminSchema(
                admin=AdminRight.previous
            )
    
    finally:
        return result.dict()

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

        if acc['Project ID'] == '':
            continue

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

        user_result = []

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
                user_result.append(__schema.dict())
            except:
                logger.info(f"error translating userright: {user['username']}, {right['SystemID']}")

        #postprocess this user to remove duplicates
        user_result_keep = consolidate_duplicate_rights(user_result)

        result.extend(user_result_keep)

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

#UQMP OHS Checklist, New Worker OHS Induction Checklist, X-ray training request
KNOWN_FORMS = {
    15: 'UQMP',
    79: 'OH&S',
    149: 'X-ray',
}

def validate_training_requests(rims_request_data: list[dict]) -> list[dict]:
    """
    validate return from training request api list 
    """
    result = []

    for request in rims_request_data:

        #NB this might make more sense in services
        if request["reqType"] is None or request["reqType"] == '':
            try:
                request_type = KNOWN_FORMS[int(request["formId"])]
            except:
                request_type = ''
        else:
            request_type = request["reqType"]

        schema = schemas.TrainingRequestReceiveSchema(
            id = request["reqId"],
            date = parse_rims_date(request["reqDate"]),
            new = request["reqNew"],
            type = request_type,
            form_id = request["formId"],
            form_name = request["formName"],
            user_id = request["userId"],
        )

        result.append(schema.dict())
    
    return result


def trequest_extract_fields_by_column(request_data: dict, form_id: int) -> dict:
    """
    extract desired fields from training request form data
    
    temporary, this may need to be a whole module with own schema to handle multiple forms

    DEPRECATED
    """    
    result = {}
    use_keys = []

    if form_id == 79:   #new worker induction form
        use_keys = ['Q3']
    else:
        logger.error(f"unrecognised training form id: {form_id} at training request parser")

    for key in use_keys:
        try:
            result[key] = request_data[key]
        except:
            logger.error(f"key {key} not found in request {request_data['Request ID']}", exc_info=True)
    
    return result


def parse_tform_responses(request_data: list[dict]) -> list[dict]:
    """
    parse training form results and compress from:

        [ {id, question, answer}, {id, question, answer}, {id, question, answer} ]
    to:
        [id, {q:a, q:a, q:a}]
    
    """    
    tforms = []


    localresult={}
    for qa in request_data:
            try:
                id = int(rims_link_extract_value(qa['Request ID']))

                if localresult.get('id') == id:
                    pass

                elif localresult.get('id') is None:
                    localresult['id'] = id

                elif isinstance(id, int):
                    tforms.append(localresult)
                    localresult = {}
                    localresult['id'] = id

                else:
                    raise ValueError(f'unexpected id encountered by training form parser {id}')

                localresult[rims_form_get_final_line(qa['Question'])] = qa['Answer']

            except:
                logger.warn(f"error parsing training form {qa['Request ID']}")

    #check for duplicates
    seen = set()
    result = []

    for tform in tforms:
        id = tform['id']
        
        if id in seen:
            logger.warn(f"Duplicate trequest id entries found for {tform['id']}, discarding older version")
        else:
            result.append(tform)
        
        seen.add(id)

    return result


def tform_data_by_id(tform_data: list[dict], tform_id: int) -> dict:
    """
    find a tform by ID and return data 
    """
    for tform in tform_data:
        try:
            if tform['id'] == tform_id:
                result = copy.deepcopy(tform)
                del result['id']
                return result
            else:
                pass
        except:
            logger.warn(f"failure locating data for training form {tform_id}")
            return {}

def validate_trequest_list(rims_request_data: list[dict], tform_data: list[dict]) -> list[dict]:
    """
    validate return from training request form report 
    """
    result = []

    for request in rims_request_data:

        trequest_id = int(rims_link_extract_key(request["Request ID"], 'trainreq'))   
        tform_content = tform_data_by_id(tform_data, trequest_id)

        schema = schemas.TrainingRequestReceiveFormDataSchema(
            id = trequest_id,
            date = parse_rims_date(request["Date"]),
            user_fullname = rims_strip_username_brackets(request["User"]),
            form_data = tform_content,
        )

        result.append(schema.dict())
    
    return result
