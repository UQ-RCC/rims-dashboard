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
    get usage data within dates
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
        df.to_hdf(file,key='df',mode='w')

    return df

def report_data():
    return user_data, project_data

def gather_userlists():
    """
    get lists of instruments and ids

    needs full_data local var
    """
    uid_list = user_data['id']
    username_list = user_data['name']

    if not np.all(uid_list.unique() == uid_list):
        raise ValueError("non-unique UID in list")

    username_list = username_list.tolist()
    uid_list = uid_list.tolist()

    return uid_list, username_list

def query_user(uid: int):
    result = rims.get_user_by_id(uid)
    return result

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

def gather_projectlists():
    """
    get lists of instruments and ids

    needs full_data local var
    """
    pid_list = project_data['ProjectRef']
    pname_list = project_data['ProjectName']

    if not np.all(pid_list.unique() == pid_list):
        raise ValueError("non-unique UID in list")

    pid_list = pid_list.tolist()
    pname_list = pname_list.tolist()

    return pid_list, pname_list

def get_systems_df():
    """
    get  data 
        use database if present
        request from RIMS API if not
    """    
    #NB NOT WORKING
    #pitschi code extracts as a set, pd expects json

    filename=f"systems.h5"
    file = os.path.join(DATA_DIR, filename)

    if os.path.isfile(file):
        df = pd.read_hdf(file, 'df')
    else:
        data=rims.get_systems()
        df = pd.DataFrame.from_dict(data)
        df.to_hdf(file,key='df',mode='w')

    return df










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