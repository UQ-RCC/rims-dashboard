import sys, os
from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
import dash_daq as daq
#from dash_bootstrap_templates import load_figure_template
import pandas as pd
import plotly.express as px
import numpy as np
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import rimsdash.usergather as gather
import rimsdash.visualisations as vis
import rimsdash.rims as rims
import rimsdash.collate as collate
import frontend.lightboards as lightboards

#--------------
#SETUP
#--------------

colorlist = lightboards.colorlist

css = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'

theme = dbc.themes.PULSE

app = Dash(__name__,
            external_stylesheets=[theme, css])

server = app.server

#--------------
#DATA
#--------------

options=collate.populate_userdropdown()

user_dropdown = dcc.Dropdown(options=options,
                            value='s4595555')

project_table = dash_table.DataTable(id='project-table', style_as_list_view=True,)


app.layout = html.Div(
    [
        html.Header([
            html.Div([
                    html.H1('RIMS dashboard'),    
            ], id="title-container" )
        ], id="mainheader"),
        html.Div([
            html.H5('Select your username:'),
            user_dropdown,
        ], id="uselect-container"),
        html.Div([
            lightboards.primary_dash,
            lightboards.rights_dash,
            lightboards.project_dash
        ], id="light-container"),
        html.Div([
            html.H5('Project data:'),        
            project_table,            
        ], id='table-container'),
        
        #variable to hold dash-state
        dcc.Store(id='dash_state_core'),
        dcc.Store(id='dash_state_access'),
        dcc.Store(id='dash_state_project'),
    ], id='container'
)


@app.callback(
    Output(dcc.Store, 'dash_state_core'),
    Output(dcc.Store, 'dash_state_access'),    
    Output(dcc.Store, 'dash_state_project'),
    Input(component_id=user_dropdown, component_property='value')
)
def get_dash_state(user_login):

    state_core, state_access, state_project = collate.dash_state(user_login)

    return json.dumps(state_core), state_access, state_project

    


@app.callback(
    Output('ind-proj-active', 'color'),
    Output('ind-proj-acc', 'color'),    
    Output('ind-proj-ohs', 'color'),    
    Output('ind-proj-rdm', 'color'),        
    Output('ind-proj-phase-0', 'color'),      
    Output('ind-proj-phase-1', 'color'),   
    Output('ind-proj-phase-2', 'color'),   
    Output('ind-proj-phase-3', 'color'),   
    Input('dash_state_project', 'data')
)
def assign_project_lights(user_login):
    c1=colorlist.neutral
    c2=colorlist.neutral
    c3=colorlist.neutral
    c4=colorlist.neutral
    c5=colorlist.neutral
    c6=colorlist.neutral
    c7=colorlist.neutral
    c8=colorlist.neutral

    user_projects = rims.get_user_projects(user_login)

    df = gather.gather_projectdetails(user_projects[0])
    details = df.to_dict('records')[0]

    #bunch of if statements

    return c1, c2, c3, c4, c5, c6, c7, c8


@app.callback(
    Output('ind-acc-hawk', 'color'),
    Output('ind-acc-aibn', 'color'),    
    Output('ind-acc-chem', 'color'),    
    Output('ind-acc-qbp', 'color'),        
    Input('dash_state', 'data')
)
def assign_userrights_lights(user_login):
    LABID_LIST = [ 65, 68, 69, 70 ]
    c1=colorlist.neutral
    c2=colorlist.neutral
    c3=colorlist.neutral
    c4=colorlist.neutral

    for lab in LABID_LIST:
        #access as key=lab
        #if value in A, N, S
        #color = success
        #else: color=neutral
        pass

    user_projects = rims.get_user_projects(user_login)
    
    return c1, c2, c3, c4

@app.callback(
    Output('ind-prim-proj', 'color'),
    Output('ind-prim-user', 'color'),    
    Input('dash_state', 'data')
)
def assign_core_lights(user_login):
    c1=colorlist.neutral
    c2=colorlist.neutral
    pass

    return c1, c2




#TO-DO "Akefe Isaac" fails with callback error, list index out of range

@app.callback(
    Output('ind-prim-proj', 'color'),
    Input(component_id=user_dropdown, component_property='value')
)
def assign_core_proj(user_login):
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



@app.callback(
    Output('ind-prim-proj', 'value'),
    Input(component_id=user_dropdown, component_property='value')
)
def update_output(user_login):
    user_projects = rims.get_user_projects(user_login)
    print(user_projects)
    if user_projects == [] or user_projects == [-1]:
        return False
    else:
        return True





def entry_main():
    app.run_server(debug=False, dev_tools_hot_reload=False)

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=False)