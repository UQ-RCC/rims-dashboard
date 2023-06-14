import pandas as pd
import plotly.express as px
import rimsdash.rims as rims
import datetime

RIMS_CUTOFF=datetime.date(2022,6,1)     #date where internal groupid changed
CMM_GROUP_ID=2              #known group ID for ppms internal usage
UQRI_GROUP_ID=731           #known group ID for rims internal usage

def count_hours(df, instrument_name, date):
    date_mask = df['date'] == pd.Timestamp(date)
    instrument_mask = df['Instrument Name'] == instrument_name

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

    return(user_hours, internal_hours, user, internal)