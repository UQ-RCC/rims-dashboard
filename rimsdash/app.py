import sys, os
from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import rimsdash.gather as gather
import rimsdash.visualisations as vis

temp_id=126

app = Dash()
server = app.server

___, ___, full_data = gather.get_usage(temp_id)
iname_list = full_data['Instrument Name'].unique()
iindex_list = full_data['Instrument ID'].unique()

iname_list = iname_list.tolist()
iindex_list = iindex_list.tolist()

instr_dropdown = dcc.Dropdown(options=sorted(iname_list),
                            value='CHEM XFM iXRF SYSTEMS')

app.layout = html.Div(children=[
    html.H1(children='Instrument usage dashboard'),
    instr_dropdown,
    dcc.Graph(id='usage-graph')
])
#    dcc.Graph(id='annual-graph')

@app.callback(
    Output(component_id='usage-graph', component_property='figure'),
    Input(component_id=instr_dropdown, component_property='value')
)
def update_usage_graph(instrument_name):

    instrument_id = iindex_list[iname_list.index(instrument_name)]

    monthly_usage, annual_usage, full_data = gather.get_usage(instrument_id)

    fig = vis.usage_bar(monthly_usage)

    return fig

"""
@app.callback(
    Output(component_id='annual-graph', component_property='figure'),
    Input(component_id=instr_dropdown, component_property='value')
)
def update_annual_graph(instrument_name):

    instrument_id = iindex_list[iname_list.index(instrument_name)]

    monthly_usage, annual_usage, full_data = gather.get_usage(instrument_id)

    fig = vis.usage_bar(annual_usage)

    return fig
"""

def entry_main():
    app.run_server(debug=False)

if __name__ == '__main__':
    app.run_server(debug=True)