import sys
import os
import datetime
import calendar
import pandas as pd

import rimsdash.rims as rims
import rimsdash.analytics as analytics

BASE_DIR=os.path.dirname(os.path.realpath(os.path.dirname(__file__)))
DATA_BASE='data/'
DATA_DIR=os.path.join(BASE_DIR, DATA_BASE)

START_YEAR = 2019

def get_dataframe(start, end):
    """
    get usage data within dates
        use database if present
        request from RIMS API if not
    """    
    filename=f"data_{start.strftime('%Y-%m')}.h5"
    file = os.path.join(DATA_DIR, filename)

    if os.path.isfile(file):
        df = pd.read_hdf(file, 'df')
    else:
        data=rims.get_usage_per_project(start,end)
        df = pd.DataFrame.from_dict(data)
        df['date'] = pd.Timestamp(start)
        df.to_hdf(file,key='df',mode='w')

    return df

def get_sessionlist(start_date=datetime.date(START_YEAR, 1, 1), end_date=datetime.datetime.today()):
    """
    retrieve full list of sessions from local cache / API

    note: currently returns whole years inclusive
    """  
    start_year = int(start_date.strftime('%Y'))
    current_year = int(end_date.strftime('%Y'))

    years = range(start_year, current_year+1)
    months = range(1,12+1)

    filename=f"db_full.h5"
    file = os.path.join(DATA_DIR, filename)

    if os.path.isfile(file):      
    #future: check data against most recent two months and update if needed      
        full_data = pd.read_hdf(file, 'df')
    else:
        first_request = True
        for year in years:
            for month in months:
                __, last_day=calendar.monthrange(year, month)
                start=datetime.date(year, month, 1)
                end=datetime.date(year, month, last_day)

                local = get_dataframe(start, end)

                if first_request:
                    full_data = local
                    first_request = False
                else:
                    full_data = pd.concat([full_data, local])

        print("WRITING DATA")
        full_data.to_hdf(file,key='df',mode='w')

    return  full_data

def get_instrument_lists():
    """
    get lists of instruments and ids

    needs full_data local var
    """
    iname_list = full_data['Instrument Name'].unique()
    iindex_list = full_data['Instrument ID'].unique()

    iname_list = iname_list.tolist()
    iindex_list = iindex_list.tolist()

    return iname_list, iindex_list


def get_usage(instrument_id, start_date=datetime.date(START_YEAR, 1, 1), end_date=datetime.datetime.today()):
    """
    get monthly and annual datasets

    needs full_data local var
    """
    monthly, annual = analytics.get_usage(full_data, instrument_id, start_date, end_date)

    return monthly, annual

def backend_load():
    """
    retrieve full list of sessions from local cache / API

    note: currently returns whole years inclusive
    """  
    full_data = get_sessionlist()

    return full_data


#load the full dataset once and hold in local memory
#   prevents concurrent reads from hd5 on simultaneous get_usage calls
full_data = backend_load()