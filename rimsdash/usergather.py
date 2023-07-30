import sys
import os
import datetime
import calendar
import pandas as pd
import numpy as np

import rimsdash.rims as rims
import rimsdash.analytics as analytics

BASE_DIR=os.path.dirname(os.path.realpath(os.path.dirname(__file__)))
DATA_BASE='data/'
DATA_DIR=os.path.join(BASE_DIR, DATA_BASE)


def get_userdata_df():
    """
    get user data
        use database if present
        request from RIMS API if not
    """    
    filename=f"users.h5"
    file = os.path.join(DATA_DIR, filename)

    if os.path.isfile(file):
        df = pd.read_hdf(file, 'df')
    else:
        data=rims.get_userlist()
        df = pd.DataFrame.from_dict(data)
        print("--------dropping------")
        df = df.drop(columns=['phone'])
        df.to_hdf(file,key='df',mode='w')
    return df

def get_projects_df():
    """
    get usage data within dates
        use database if present
        request from RIMS API if not
    """    
    filename=f"projects.h5"
    file = os.path.join(DATA_DIR, filename)

    if os.path.isfile(file):
        df = pd.read_hdf(file, 'df')
    else:
        data=rims.get_projects()
        df = pd.DataFrame.from_dict(data)
        df.to_hdf(file,key='df',mode='w')

    return df

def get_systems_df():
    """
    get  data 
        use cache if present
        request from RIMS API if not
    """    
    filename=f"systems.h5"
    file = os.path.join(DATA_DIR, filename)

    if os.path.isfile(file):
        df = pd.read_hdf(file, 'df')
    else:
        data=pumapi_wrapper(rims.get_systems())

        df = pd.DataFrame.from_dict(data)
        df.to_hdf(file,key='df',mode='w')

    return df

def query_user(uid: int):
    result = rims.get_user_by_id(uid)
    return result

def get_user_rights_df(ulogin: str):

    raw = rims.get_user_rights(ulogin)

    df = pd.DataFrame(raw.items(), columns=['systemid', 'access_level'])

    return df

def gather_userlists():
    """
    get paired lists of user logins and user full names

    uses full_data local var
    """
    login_list = user_data['login']
    name_list = user_data['name']

    if not np.all(login_list.unique() == login_list):
        raise ValueError("non-unique UID in list")

    login_list = login_list.tolist()
    name_list = name_list.tolist()

    return login_list, name_list

def gather_projectlists():
    """
    get paired lists of projects and project ids

    uses full_data local var
    """
    pid_list = project_data['ProjectRef']
    pname_list = project_data['ProjectName']

    if not np.all(pid_list.unique() == pid_list):
        raise ValueError("non-unique UID in list")

    pid_list = pid_list.tolist()
    pname_list = pname_list.tolist()

    return pid_list, pname_list

def gather_projectdetails(pid: int):
    
    selected = project_data[project_data['ProjectRef'] == pid]

    return selected


def pumapi_wrapper(raw_data):
    """
    converts dict-of-dicts returned by pitschi PUMAPI functions into simple dict
    """
    data=[]

    for key, value in raw_data.items():
            data.append(value)

    return data


def report_data():
    """
    reads out local vars
    """    
    return user_data, project_data


def backend_load():
    """
    retrieve data from local cache / API
    """  
    user_data = get_userdata_df()
    project_data = get_projects_df()

    return user_data, project_data


#load the full dataset once and hold in local memory
#   prevents concurrent reads from hd5 on simultaneous get_usage calls
user_data, project_data = backend_load()