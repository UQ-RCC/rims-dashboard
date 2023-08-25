import sys, os
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_auth
import json

from dash import Dash, html, dcc, Input, Output, dash_table

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import dashboard.lightboards as lightboards
import dashboard.auth as auth

#import rimsdash.usergather as gather
#import rimsdash.rims as rims
#import rimsdash.collate as collate


#--------------
#SETUP
#--------------

VALID_USERNAME_PASSWORD_PAIRS = auth.get_auth_details()
css = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'
theme = dbc.themes.PULSE


dash_app = Dash(__name__,
        routes_pathname_prefix='/',
        external_stylesheets=[theme, css])

auth = dash_auth.BasicAuth(
    dash_app,
    VALID_USERNAME_PASSWORD_PAIRS
)

server=dash_app.server

#--------------
#DATA
#--------------

#API RETURN HERE
userlist=collate.populate_userdropdown()

user_dropdown = dcc.Dropdown(options=userlist,
                            value='s4595555')

#s4595555   experienced user
#t.blach    fee-for-service user

project_table = dash_table.DataTable(id='project-table', style_as_list_view=True,)

dash_app.layout = html.Div(
    [
        html.Header([
            html.Div([
                    html.H1('Centre for Microscopy and Microanalysis', id="main-title"),      #style={'text-align': 'center', 'align': 'center'}
            ], id="title-container" )
        ], id="main-header"),
        html.Div([
            html.Div([
                html.Div([
                    html.H5('Username:'),
                    user_dropdown,
                ], id="uselect-container"),
                html.Div([
                    lightboards.primary_dash,
                    lightboards.rights_dash,
                    lightboards.project_dash
                ], id="panel-container"),
                html.Div([
                    html.H5('Project data:'),        
                    project_table,            
                ], id='table-container'),
            ], id='content-container'),
        ], id='page-container'),
        #variable to hold dash-state
        dcc.Store(id='dash_state_core'),
        dcc.Store(id='dash_state_access'),
        dcc.Store(id='dash_state_project'),
    ], id='body-container',
)

@dash_app.callback(
    Output('dash_state_core', 'data'),
    Output('dash_state_access', 'data'),    
    Output('dash_state_project', 'data'),
    Input(component_id=user_dropdown, component_property='value')
)
def get_dash_state(user_login):

    #API RETURN HERE
    state_core, state_access, state_project = collate.dash_state(user_login)

    return json.dumps(state_core), json.dumps(state_access), json.dumps(state_project)


@dash_app.callback(
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
def assign_project_lights(state_raw: str):

    state = json.loads(state_raw)

    if len(state) != 8:
        raise ValueError("unexpected number of states")    

    colours = []

    for value in state:
        colours.append(lightboards.colour_from_istate(value))

    return tuple(colours)

@dash_app.callback(
    Output('ind-acc-hawk', 'color'),
    Output('ind-acc-aibn', 'color'),    
    Output('ind-acc-chem', 'color'),    
    Output('ind-acc-qbp', 'color'),        
    Input('dash_state_access', 'data')
)
def assign_accessrights_lights(state_raw: str):

    state = json.loads(state_raw)

    if len(state) != 4:
        raise ValueError("unexpected number of states")    

    colours = []

    for value in state:
        colours.append(lightboards.colour_from_istate(value))

    return tuple(colours)

@dash_app.callback(
    Output('ind-prim-user', 'color'),
    Output('ind-prim-proj', 'color'),    
    Input('dash_state_core', 'data')
)
def assign_core_lights(state_raw: str):

    state = json.loads(state_raw)

    if len(state) != 2:
        raise ValueError("unexpected number of states")    

    colours = []

    for value in state:
        colours.append(lightboards.colour_from_istate(value))

    return tuple(colours)


@dash_app.callback(
    Output(component_id='project-table', component_property='data'),
    Output(component_id='project-table', component_property='columns'),
    Input(component_id=user_dropdown, component_property='value')
)
def update_project_table(user_login):
    """
    update the monthly usage graph
    """

    #API RETURN HERE
    print(f"{user_login}")
    user_projects = rims.get_user_projects(user_login)

    print(user_projects[0])

    #API RETURN HERE
    #TODO: modified -> does not return df anymore, match to rimsboard
    project_info_df = gather.gather_projectdetails(user_projects[0])

    data = project_info_df.to_dict('records')
    columns = [{"name": i, "id": i} for i in project_info_df.columns]
    return data, columns

"""
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
        return False
"""


def entry_dev():
    dash_app.run(port=8050)

if __name__ == "__main__":
    entry_dev()