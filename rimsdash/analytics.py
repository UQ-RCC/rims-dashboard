import pandas as pd
import plotly.express as px
import rimsdash.rims as rims

CMM_GROUP_ID=731        #known group ID for internal usage
instrument_name='CHEM XFM iXRF SYSTEMS'
start_date="2023-05-01"
end_date="2023-05-31"

usage_per_project = rims.get_usage_per_project(start_date, end_date)

df = pd.DataFrame.from_dict(usage_per_project)

instrument_mask = df['Instrument Name'] == instrument_name
group_mask = df['Group ID'] == CMM_GROUP_ID
mask_billed = instrument_mask & ~group_mask
mask_internal = instrument_mask & group_mask

dff = df[mask_billed]
