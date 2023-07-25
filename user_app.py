import sys, os
from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
import dash_daq as daq
#from dash_bootstrap_templates import load_figure_template
import pandas as pd
import plotly.express as px
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import rimsdash.usergather as gather
import rimsdash.visualisations as vis
import rimsdash.rims as rims

class ColorList():
    def __init__(self):
        self.success = "#33f975"
        self.warn = "#ffb34d"
        self.fail = "#fc5959"
        self.neutral = "#BBBBBB"

colorlist = ColorList()

css = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'
theme = dbc.themes.PULSE
app = Dash(name="rimsdash",
            external_stylesheets=[theme, css])
server = app.server


uid_list, name_list = gather.gather_userlists()

def sort_paired(list1, list2):
    zipped = zip(list1, list2)           
    result1, result2 = zip(*sorted(zipped))
    return result1, result2

name_list, uid_list = sort_paired(name_list, uid_list)

options=[]

for i, uid in enumerate(uid_list):
    options.append({'label': f"{name_list[i]} ({uid_list[i]})", 'value': uid_list[i], 'search': name_list[i]})

#user_dropdown = dcc.Dropdown(options=sorted(uid_list),
#                            value='s4595555')

user_dropdown = dcc.Dropdown(options=options,
                            value='s4595555')

user_table = dash_table.DataTable()

app.layout = html.Div([
    html.H1('RIMS dashboard'),
    html.P('Select your account:'),
    user_dropdown,
    html.P('Project data:'),
    dash_table.DataTable(id='project-table', style_as_list_view=True,),    
    html.P('Project status:'),
    html.Div([
        daq.Indicator(
            id='indic-user',
            label="Account",
            size=30,
            color=colorlist.success,
            style={'width': '10%', 'display': 'inline-block'}
        ),
        daq.Indicator(
            id='indic-proj',
            label="Project",
            size=30,
            color=colorlist.warn,
            style={'width': '10%', 'display': 'inline-block'}
        ),
        daq.Indicator(
            id='indic-rights',
            label="Training",
            size=30,
            color=colorlist.fail,
            style={'width': '10%', 'display': 'inline-block'}
        ),        
        daq.Indicator(
            id='indic-ohs',
            label="Lab access",
            size=30,
            color=colorlist.neutral,
            style={'width': '10%', 'display': 'inline-block'}
        ),
        ],
        style={'width': '50%', 'display': 'inline-block'}
    ),
    html.Button(
        'On/Off',
        id='my-indicator-button-1',
        n_clicks=0
    )]
)

#TO-DO "Akefe Isaac" fails with callback error, list index out of range
@app.callback(
    Output('indic-proj', 'value'),
    Input(component_id=user_dropdown, component_property='value')
)
def update_output(user_login):
    user_projects = rims.get_user_projects(user_login)
    print(user_projects)
    if user_projects == [] or user_projects == [-1]:
        return False
    else:
        return True


@app.callback(
    Output('indic-proj', 'color'),
    Input(component_id=user_dropdown, component_property='value')
)
def project_color(user_login):
    user_projects = rims.get_user_projects(user_login)

    if user_projects == [] or user_projects == [-1]:
        return colorlist.neutral
    else:   
        df = gather.gather_projectdetails(user_projects[0])
        details = df.to_dict('records')[0]
        #note: this does not work perfectly, some fields become strings

        if bool(details['Active']) == True:
            return colorlist.success
        else:
            return colorlist.warn



@app.callback(
    Output(component_id='project-table', component_property='data'),
    Output(component_id='project-table', component_property='columns'),
    Input(component_id=user_dropdown, component_property='value')
)
def update_project_table(user_login):
    """
    update the monthly usage graph
    """
    print(f"{user_login}")
    user_projects = rims.get_user_projects(user_login)

    print(user_projects[0])

    project_info_df = gather.gather_projectdetails(user_projects[0])

    data = project_info_df.to_dict('records')
    columns = [{"name": i, "id": i} for i in project_info_df.columns]
    return data, columns


def entry_main():
    app.run_server(debug=False)

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=False)