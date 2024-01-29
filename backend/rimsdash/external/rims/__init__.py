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

def get_training_request_list() -> list[dict]:
    _rims_user_list = queries.get_training_request_list()

    user_list = translate.validate_training_requests(_rims_user_list)

    return user_list


def get_project_details() -> list[dict]:
    _rims_project_details = queries.get_project_details()

    project_details = translate.validate_project_details(_rims_project_details)

    return project_details


def get_admin_status(username: str) -> dict:

    _system_to_check = config.get('ppms','system_for_admin_check') 

    result = False

    _rights_dict = queries.get_admin_rights(username, _system_to_check)

    result = translate.validate_admin_check(_rights_dict)
    
    return result


def get_project_accounts() -> list[dict]:

    __account_data = queries.get_chartstring_data()

    result = translate.validate_account_list(__account_data)

    return result


def get_user_rights_list() -> list[dict]:

    __rights_data = queries.get_rights_by_user()

    result = translate.validate_user_rights_list(__rights_data)

    return result


def get_user_projects_list() -> list[dict]:

    user_projects_data = queries.get_projects_by_user()

    result = translate.validate_user_projects_list(user_projects_data)

    return result


def get_trequest_content_list(form_id: int) -> list[dict]:

    trequest_data = queries.get_trequest_content(form_id)

    result = translate.validate_trequest_list(trequest_data, form_id)

    return result