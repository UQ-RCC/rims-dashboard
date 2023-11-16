import rimsdash.schemas as schemas

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

