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

logger = logging.getLogger('pitschixapi')

KEY=f"{config.get('ppms', 'api2_key')}"
CORE_ID=f"{config.get('ppms', 'core_id')}"
BASE_URL=f"{config.get('ppms','ppms_url')}"
DATE_FORMAT='%Y-%m-%d'


def get_usage_per_project(start_date=datetime.date(2022, 7, 1), end_date=datetime.date(2022, 7, 31)):
    """
    requests instrument usage per project between start and end dates from RIMS API
    returns as json
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


def get_systems():
    """
    requests system ids from RIMS API
    returns as nested dicts
    """        
    logger.debug("Querying systems")
    url = f"{BASE_URL}pumapi/"
    coreid=f"{config.get('ppms', 'core_id')}"
    key=f"{config.get('ppms', 'api2_key')}"
    payload=f"apikey={key}&action=getsystems"
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.ok:
        if response.status_code == 204:
            return {}
        else:
            # format is in csv
            _systems_text = response.text
            _csv_reader = csv.reader(_systems_text.split('\n'), delimiter=',')
            _csv_reader.__next__()
            systems = {}
            for row in _csv_reader:
                if(len(row) > 3):
                    _systemid = int(row[1])
                    _systemtype = row[2]
                    _systemname = row[3]
                    systems[_systemname] = {'systemid': _systemid, 'systemtype': _systemtype, 'systemname': _systemname}
            return systems
    return {}


def get_userlist():
    """
    requests user report from RIMS API
    returns as json
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


def get_user_by_id(uid):
    """
    requests user data by id
    returns as json
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


def get_projects(active_only = False):
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



def get_user_rights(ulogin: str):
    """
    failing? 
    """

    logger.debug("Querying systems")
    url = f"{BASE_URL}pumapi/"

    payload=f"apikey={KEY}&action=getuserrights&login={ulogin}&format=json"
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
            _permissions = { int(_line.split(":")[1]):_line.split(":")[0] for _line in _lines } #int() strips remaining carriage return
            return _permissions
    return {}


def get_user_projects(ulogin: str):
    logger.debug("Querying systems")
    url = f"{BASE_URL}pumapi/"

    payload=f"apikey={KEY}&action=getuserprojects&login={ulogin}&format=json"
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)
    if response.ok:
        if response.status_code == 204:
            return {}
        else:
                # format is pid\n
                _system_rights_text = response.text.strip()
                _lines = _system_rights_text.split('\n')
                _pids = { int(_line) for _line in _lines }  #int() strips remaining carriage return
                return _pids
    return {}



#------------------------------------------
#pitschi originals
#------------------------------------------

def get_ppms_user(login):
    url = f"{config.get('ppms', 'ppms_url')}pumapi/"
    key=f"{config.get('ppms', 'api2_key')}"
    payload=f"apikey={key}&action=getuser&login={login}&format=json"
    
    
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.ok:
        if response.status_code == 204:
            raise Exception('Not found')
        else:
            # logger.debug(f"Response: {response}")
            return response.json(strict=False)
    else:
        raise Exception('Not found')


def get_ppms_user_by_id(uid:int, coreid:int):
    logger.debug("@get_ppms_user_by_id: Querying user by id")
    url = f"{config.get('ppms', 'ppms_url')}API2/"
    key=f"{config.get('ppms', 'api2_key')}"    
    payload=f"outformat=json&apikey={key}&action=GetUserDetailsById&checkUserId={uid}&coreid={coreid}"
    
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.ok:
        if response.status_code == 204:
            return []
        else:
            return response.json(strict=False)
    return []



def get_system_rights(systemid: int):
    logger.debug("Querying systems")
    url = f"{config.get('ppms', 'ppms_url')}pumapi/"
    key=f"{config.get('ppms', 'api2_key')}"

    payload=f"apikey={key}&action=getsysrights&id={systemid}"
    print(payload)
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.ok:
        if response.status_code == 204:
            return {}
        else:
            # format is in mode:name\n
            _system_rights_text = response.text.strip()
            _lines = _system_rights_text.split('\n')
            _permissions = { _line.split(":")[1]:_line.split(":")[0] for _line in _lines }
            return _permissions
    return {}



def get_project_user(projectid: int):
    logger.debug("Querying project user")
    url = f"{config.get('ppms', 'ppms_url')}pumapi/"
    payload=f"apikey={config.get('ppms', 'ppms_key')}&action=getprojectusers&withdeactivated=false&projectid={projectid}"
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.ok:
        if response.status_code == 204:
            return []
        else:
            response_txt = response.text
            return response_txt.strip().split("\n")
    else:
        return []

def get_project_members(projectid: int):
    """
    Similar to project_user but with user id as well
    """
    logger.debug("Querying project user")
    url = f"{config.get('ppms', 'ppms_url')}pumapi/"
    payload=f"apikey={config.get('ppms', 'ppms_key')}&action=getprojectmember&projectid={projectid}"
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.ok:
        if response.status_code == 204:
            return []
        else:
            response_txt = response.text
            _csv_reader = csv.reader(response_txt.split('\n'), delimiter=',')
            _csv_reader.__next__()
            members = []
            for row in _csv_reader:
                if(len(row) > 8):
                    _userid = int(row[1])
                    _userlogin = row[8]
                    members.append({'id': _userid, 'login': _userlogin})
            return members
    else:
        return []
    
def get_rdm_collection(coreid: int, projectid: int):
    url = f"{config.get('ppms', 'ppms_url')}API2/"
    payload=f"apikey={config.get('ppms', 'api2_key')}&action={config.get('ppms', 'qcollection_action')}&projectId={projectid}&coreid={coreid}&outformat=json"
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.ok:
        if response.status_code == 204:
            return ""
        qcollection = ""
        if len(response.json()) > 0:
            qcollection = response.json(strict=False)[0].get(config.get('ppms', 'q_collection_field'))
        return qcollection
    return ""