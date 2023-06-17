import sys
import os
import datetime
import calendar
import pandas as pd
import numpy as np
import dateutil.relativedelta as relativedelta

import rimsdash.rims as rims
import rimsdash.analytics as analytics

BASE_DIR=os.path.dirname(os.path.realpath(os.path.dirname(__file__)))
DATA_BASE='data/'
DATA_DIR=os.path.join(BASE_DIR, DATA_BASE)

START_YEAR = 2019
RIMS_CUTOFF=datetime.date(2022,6,1)     #date where internal groupid changed
CMM_GROUP_ID=2              #known group ID for ppms internal usage
UQRI_GROUP_ID=731           #known group ID for rims internal usage
XFM_ID=126

def count_hours(df, instrument_id: int, date):
    """
    get user and internal usage for a given month
    """

    date_mask = df['date'] == pd.Timestamp(date)
    instrument_mask = df['Instrument ID'] == instrument_id

    if date < RIMS_CUTOFF:
        internal_group_id = CMM_GROUP_ID
    else:
        internal_group_id = UQRI_GROUP_ID

    group_mask = df['Group ID'] == internal_group_id

    mask_internal = instrument_mask & date_mask & group_mask 
    mask_user = instrument_mask & date_mask & ~group_mask 

    user = df[mask_user]
    internal = df[mask_internal]

    user_hours = user['Total hours booked'].sum()
    internal_hours = internal['Total hours booked'].sum()

    return user_hours, internal_hours, user, internal


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


def get_usage(instrument_id=XFM_ID):
    """
    collate monthly & yearly usage for given instrument ID
    """  
    current_year = int(datetime.datetime.today().strftime('%Y'))
    current_month = int(datetime.datetime.today().strftime('%m'))
    current_day = int(datetime.datetime.today().strftime('%d'))    

    years = range(START_YEAR, current_year+1)
    months = range(1,12+1)

    user_hours = np.zeros(len(years)*len(months), dtype=np.float32)
    internal_hours = np.zeros(len(years)*len(months), dtype=np.float32) 
    datelist = []

    filename=f"db_id{instrument_id}.h5"
    file = os.path.join(DATA_DIR, filename)

    if os.path.isfile(file):      
    #future: check data against most recent two months and update if needed      
        full_data = pd.read_hdf(file, 'df')
        request_frames = False
    else:
        request_frames = True
        first_request = True

    index=0
    for year in years:
        for month in months:
            __, last_day=calendar.monthrange(year, month)
            start=datetime.date(year, month, 1)
            end=datetime.date(year, month, last_day)
            datelist.append(start)

            if request_frames:
                local = get_dataframe(start, end)

                if first_request:
                    full_data = local
                    first_request = False
                else:
                    full_data = pd.concat([full_data, local])

            user_hours[index], internal_hours[index], ___, ____ = count_hours(full_data, instrument_id, start)

            index += 1

    monthly = pd.DataFrame({'date':datelist, 'user_hours':user_hours, 'internal_hours':internal_hours})

    monthly['date'] = pd.to_datetime(monthly['date'])

    if request_frames:
        full_data.to_hdf(file,key='df',mode='w')

    annual = monthly.resample('Y', on='date').sum()


    temp = annual

    annual= temp.reset_index(level='date')


    return monthly, annual, full_data