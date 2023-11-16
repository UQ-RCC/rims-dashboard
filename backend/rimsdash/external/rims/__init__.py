import rimsdash.external.rims.queries as queries
import rimsdash.external.rims.translate as translate

import rimsdash.config as config

def get_system_list() -> list[dict]:
    _rims_system_data = queries.get_systems()

    system_list = translate.validate_systems(_rims_system_data)

    return system_list


def get_user_list() -> list[dict]:
    _rims_user_list = queries.get_user_list()

    user_list = translate.validate_user_list(_rims_user_list)

    return user_list


def get_project_list() -> list[dict]:
    _rims_project_list = queries.get_project_list()

    project_list = translate.validate_project_list(_rims_project_list)

    return project_list



def get_project_details() -> list[dict]:
    _rims_project_details = queries.get_project_details()

    project_details = translate.validate_project_details(_rims_project_details)

    return project_details


def get_admin_status(username: str) -> bool:

    _system_to_check = config.get('ppms','system_for_admin_check') 

    result = False

    _rights_dict = queries.get_admin_rights(username, _system_to_check)

    result = translate.validate_admin_check(_rights_dict)
    
    return result

