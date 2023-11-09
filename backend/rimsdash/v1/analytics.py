import datetime
import pandas as pd
import numpy as np

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


def get_usage(full_data, instrument_id: int, start_date=datetime.date(START_YEAR, 1, 1), end_date=datetime.datetime.today()):
    """
    extract monthly and annual usage stats for timeperiod
    """    
    current_year = int(datetime.datetime.today().strftime('%Y'))

    years = range(START_YEAR, current_year+1)
    months = range(1,12+1)

    user_hours = np.zeros(len(years)*len(months), dtype=np.float32)
    internal_hours = np.zeros(len(years)*len(months), dtype=np.float32) 
    datelist = []

    index=0
    for year in years:
        for month in months:
            start=datetime.date(year, month, 1)
            datelist.append(start)

            user_hours[index], internal_hours[index], ___, ____ = count_hours(full_data, instrument_id, start)

            index += 1

    monthly = pd.DataFrame({'date':datelist, 'user_hours':user_hours, 'internal_hours':internal_hours})

    monthly['date'] = pd.to_datetime(monthly['date'])    

    annual = monthly.resample('Y', on='date').sum()

    temp = annual

    annual= temp.reset_index(level='date')

    #wind back by 1y
    annual['date'] = annual['date'] - pd.Timedelta(days=364)

    return monthly, annual