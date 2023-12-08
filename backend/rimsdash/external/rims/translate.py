import re 
import logging

import rimsdash.schemas as schemas

logger = logging.getLogger('rimsdash')

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
            name = user['name'],
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

        _schema = schemas.ProjectCreateSchema(
            id = project['ProjectRef'],
            title = project['ProjectName'],
            phase = project['Phase'],
            active = project['Active'],
            bcode = project['Bcode'],
            affiliation = project['Affiliation'],
            type = project['ProjectType'],
            group = project['ProjectGroup'],
            core_id = project['CoreFacilityRef'],
            description = project['Descr'],
        )

        result.append(_schema.to_dict())
    
    return result

def validate_admin_check(rights_dict: dict) -> bool:
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
    
    NB: API currently returns all facilities
        including hardcoded filter for CMM only
    """

    result = []

    for project in rims_project_details:

        #filter for projects in CMM
        if "CMM" in project['Visibility'][:4]:

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

    NB: accounts do not have ids yet as this is a primary key created by rimsdash

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
        #   ( use a dummy id )       
        try:
            __account_schema = schemas.account_schema.AccountReceiveSchema(
                id = -1,
                bcode = rims_link_extract_key(acc['Project Account'], 'bcode'),
            )
            account_dict = __account_schema.dict()

        except:
            if __valid:                          
                logger.warn(f"account read failed for valid projaccount {acc['Project ID']}, {acc['Project Account']}, {acc['Group PI']}")
            continue

        #validate the join and validity
        __join_schema = schemas.projectaccount_schema.ProjectAccountReceiveSchema(
            account_id = account_dict['id'],
            project_id = project_dict['id'],
            valid = __valid,
        )
        projectaccount = __join_schema.dict()

        #rename the pid key to avoid conflicts later
        project_dict['project_id'] = project_dict['id']   

        #drop the original project id and the dummy account ids
        del project_dict['id']
        del account_dict['id']
        del projectaccount['account_id']

        #merge in the account and project dicts
        projectaccount.update(account_dict)
        projectaccount.update(project_dict)
        
        result.append(projectaccount)

    return result