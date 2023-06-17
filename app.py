from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import numpy as np

import rimsdash.gather as gather
import rimsdash.analytics as analytics

temp_id=126

app = Dash()

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


@app.callback(
    Output(component_id='usage-graph', component_property='figure'),
    Input(component_id=instr_dropdown, component_property='value')
)
def update_graph(instrument_name):

    instrument_id = iindex_list[iname_list.index(instrument_name)]

    monthly_usage, annual_usage, full_data = gather.get_usage(instrument_id)

    #print(f"DEBUG: {instrument_id}")
    #print(monthly_usage)

    fig = analytics.usage_bar(monthly_usage)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

