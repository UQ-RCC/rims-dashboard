"""
Adapted from https://github.com/UQ-RCC/pitschi-xapi
c. 2021, The University of Queensland 
Apache 2.0
"""

import json, csv
import requests
import datetime
import logging
import rimsdash.config as config
import rimsdash.utils as utils
from rimsdash.schemas import SystemReceiveSchema, UserReceiveSchema

#from .translator import translate_projectsv2


logger = logging.getLogger('rimsdash')

KEY=f"{config.get('ppms', 'api2_key')}"
CORE_ID=f"{config.get('ppms', 'core_id')}"
BASE_URL=f"{config.get('ppms','ppms_url')}"
DATE_FORMAT='%Y-%m-%d'



def get_usage_per_project(start_date=datetime.date(2022, 7, 1), end_date=datetime.date(2022, 7, 31)):
    """
    requests instrument usage per project between start and end dates from RIMS API
    returns json
    """    
    REPORT_NO=1064
    date_format='%Y-%m-%d'
    url=f"{BASE_URL}API2/"
    return_format=f"json"
    payload=f"apikey={KEY}&action=Report{REPORT_NO}&startDate={start_date.strftime(date_format)}&endDate={end_date.strftime(date_format)}&dateformat=print&outformat={return_format}&coreid={CORE_ID}"
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.ok:
        if response.status_code == 204:
            raise Exception('Not found')
        else:
            return response.json(strict=False)
    else:
        raise Exception('Not found')


def get_chartstring_data() -> list[dict]:
    """
    requests chartstring info from RIMS API
    """    
    REPORT_NO=56  #authorised chart strings
    url=f"{BASE_URL}API2/"
    return_format=f"json"
    payload=f"apikey={KEY}&action=Report{REPORT_NO}&dateformat=print&outformat={return_format}&coreid={CORE_ID}"
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.ok:
        if response.status_code == 204:
            raise Exception('Not found')
        else:
            return response.json(strict=False)

    else:
        raise Exception('Not found')



def get_rights_by_user() -> list[dict]:
    """
    requests user rights report from RIMS API
    """    
    REPORT_NO=1527  #user rights
    url=f"{BASE_URL}API2/"
    return_format=f"json"
    payload=f"apikey={KEY}&action=Report{REPORT_NO}&dateformat=print&outformat={return_format}&coreid={CORE_ID}"
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.ok:
        if response.status_code == 204:
            raise Exception('Not found')
        else:
            return response.json(strict=False)

    else:
        raise Exception('Not found')


def get_projects_by_user() -> list[dict]:
    """
    requests user projects report from RIMS API
    """    
    REPORT_NO=1526  #project membership
    url=f"{BASE_URL}API2/"
    return_format=f"json"
    payload=f"apikey={KEY}&action=Report{REPORT_NO}&dateformat=print&outformat={return_format}&coreid={CORE_ID}"
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.ok:
        if response.status_code == 204:
            raise Exception('Not found')
        else:
            return response.json(strict=False)

    else:
        raise Exception('Not found')





def get_systems() -> list[dict]:
    """
    requests system ids from RIMS API
    """        
    url = f"{BASE_URL}pumapi/"
    coreid=f"{config.get('ppms', 'core_id')}"
    key=f"{config.get('ppms', 'api2_key')}"
    payload=f"apikey={key}&action=getsystems"
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    result = []
    if response.ok:
        if response.status_code == 204:
            return result
        else:
            # response format is csv
            _response_text = response.text
            _csv_reader = csv.reader(_response_text.split('\n'), delimiter=',')
            _csv_reader.__next__()

            for row in _csv_reader:
                if(len(row) > 3):
                    _id = int(row[1])
                    _type = row[2]
                    _name = row[3]
                    result.append({"id": _id, "type": _type, "name": _name })
            return result
    else:
        raise Exception('RIMS response not ok')


def get_pending_users():
    """
    requests list of account creation requests
        does not contain logins, emails etc

    returns list of dicts
    """    
    url=f"{BASE_URL}API2/"
    return_format=f"json"
    #NB: ignores codeid and returns all users from all cores
    #   api still wants coreid even though it proceeds to ignore it
    payload=f"apikey={KEY}&action=GetAccountCreationRequests&dateformat=print&outformat={return_format}&coreid={CORE_ID}"
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.ok:
        if response.status_code == 204:
            raise Exception('Not found')
        else:
            result = []
            #strip out users from other cores before returning
            for userdict in response.json(strict=False):
                if userdict['coreid'] == int(CORE_ID):
                    result.append(userdict)
            return result
    else:
        raise Exception('Not found')


def get_user_list() -> list[dict]:
    """
    requests user report from RIMS API
    returns list-of-dicts
    fields:
        id, name, email, phone, account number, group, affiliation, active
    """    
    REPORT_NO=1335  #user list
    url=f"{BASE_URL}API2/"
    return_format=f"json"
    payload=f"apikey={KEY}&action=Report{REPORT_NO}&dateformat=print&outformat={return_format}&coreid={CORE_ID}"
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.ok:
        if response.status_code == 204:
            raise Exception('Not found')
        else:
            return response.json(strict=False)

    else:
        raise Exception('Not found')



def get_userdata_by_id(uid):
    """
    requests user data by id
    returns json
    """    
    url=f"{BASE_URL}API2/"
    return_format=f"json"

    payload=f"apikey={KEY}&action=GetUserDetailsById&checkUserId={uid}&outformat={return_format}&coreid={CORE_ID}"

    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.ok:
        if response.status_code == 204:
            raise Exception('Not found')
        else:
            return response.json(strict=False)
    else:
        raise Exception('Not found')

def get_project_details(active_only = False) -> list[dict]:
    """
    request full project list incl basic details

    returns list of dicts

    additional: List of projects -> has description, bcode
    """    
   
    REPORT_NO=645  #projectdetailsv2
    url=f"{BASE_URL}API2/"
    return_format=f"json"
    payload=f"apikey={KEY}&action=Report{REPORT_NO}&dateformat=print&outformat={return_format}&coreid={CORE_ID}"
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.ok:
        if response.status_code == 204:
            raise Exception('Not found')
        else:
            result = response.json(strict=False)
    else:
        raise Exception('Not found')

    return result
    #translate.projectsv2(


def get_project_list(active_only = False) -> list[dict]:
    """
    request full project list incl basic details

    returns list of dicts
    """    
    logger.debug("Querying projects")

    url = f"{BASE_URL}pumapi/"

    if active_only:
        payload=f"apikey={KEY}&action=getprojects&active=True&format=json"
    else:
        payload=f"apikey={KEY}&action=getprojects&format=json"

    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.ok:
        if response.status_code == 204:
            return []
        else:
            return response.json(strict=False)
    else:
        return []


def get_admin_rights(login: str, sysid: int):
    """
    checks user's rights on a system
    field returns "ADM" if user is an admin 
    """

    url = f"{BASE_URL}pumapi/"

    payload=f"apikey={KEY}&action=rightcheck&login={login}&id={sysid}&format=json"
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.ok:
        if response.status_code == 204:
            return {}
        else:
            _text = response.text.strip()
            _lines = _text.split('\r\n')
            if not _lines == ['']:
                permissions = { 'rights': _lines[0], 'admin': False }
                try:
                    if _lines[1] == 'ADM':
                         permissions['admin'] = True
                finally:
                    return permissions
            else:
                return {}
    else:
        return {}


def get_user_rights(login: str):
    """
    get user rights by system

    returns dict
    """

    url = f"{BASE_URL}pumapi/"

    payload=f"apikey={KEY}&action=getuserrights&login={login}&format=json"
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.ok:
        if response.status_code == 204:
            return {}
        else:
            # format is right : isnt_id\n
            _system_rights_text = response.text.strip()
            _lines = _system_rights_text.split('\n')
            if not _lines == ['']:
                _permissions = { int(_line.split(":")[1]):_line.split(":")[0] for _line in _lines } #int() strips remaining carriage return
            else:
                return {}
            return _permissions
    else:
        return {}


def get_user_projects(login: str):
    """
    returns list of all projects associated with user login
    """

    url = f"{BASE_URL}pumapi/"

    payload=f"apikey={KEY}&action=getuserprojects&login={login}&format=json"
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.ok:
        if response.status_code == 204:
            return []
        else:
                # format is pid\n
                _system_rights_text = response.text.strip()
                _lines = _system_rights_text.split('\r\n')
                _pids = { _line for _line in _lines }  #int() strips remaining carriage return
                #create as set then cast to list to retain received sorting                
                result = [ utils.safecast_int(x) for x in list(_pids)]
                return result  
    return []

def get_project_users(projectid: int):
    """
    returns list of all projects associated with user login
    """

    url = f"{BASE_URL}pumapi/"

    payload=f"apikey={KEY}&action=getprojectusers&projectid={projectid}&format=json"
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.ok:
        if response.status_code == 204:
            return []
        else:
                _text = response.text.strip()
                _lines = _text.split('\r\n')
                result = [ _line for _line in _lines ]  #int() strips remaining carriage return
                return result  
    return []


def get_training_request_list() -> list[dict]:
    """
    fetches list of training requests from RIMS
    """    
    url=f"{BASE_URL}API2/"
    return_format=f"json"
    payload=f"apikey={KEY}&action=GetTrainingRequestsList&dateformat=print&outformat={return_format}&coreid={CORE_ID}"
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.ok:
        if response.status_code == 204:
            raise Exception('Not found')
        else:
            return response.json(strict=False)
    else:
        raise Exception('Not found')
