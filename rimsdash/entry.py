import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import rimsdash.rims as rims
import rimsdash.gather as gather
import pandas as pd
import rimsdash.analytics as analytics

instrument_id=126

monthly_usage, annual_usage, full_data = gather.get_usage(instrument_id)

fig = analytics.usage_bar(monthly_usage)

fig.show()