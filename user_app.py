import sys, os
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import rimsdash.usergather as gather
import rimsdash.visualisations as vis

temp_login=126

css = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'
theme = dbc.themes.PULSE
app = Dash(name="rimsdash",
            external_stylesheets=[theme, css])
server = app.server

uid_list, username_list = gather.gather_userlists()

user_dropdown = dcc.Dropdown(options=sorted(username_list),
                            value='myusername')

app.layout = html.Div(children=[
    html.H1(children='User dashboard'),
    user_dropdown,
    dcc.Graph(id='usage-graph'),
    dcc.Graph(id='annual-graph',style={'width': '90vh', 'height': '40vh'})
])
















def entry_main():
    app.run_server(debug=False)

if __name__ == '__main__':
    app.run_server(debug=True)