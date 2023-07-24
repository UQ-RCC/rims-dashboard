import sys, os
from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
#from dash_bootstrap_templates import load_figure_template
import pandas as pd
import plotly.express as px
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import rimsdash.usergather as gather
import rimsdash.visualisations as vis
import rimsdash.rims as rims

css = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'
theme = dbc.themes.DARKLY
app = Dash(name="rimsdash",
            external_stylesheets=[theme, css])
server = app.server

uid_list, login_list = gather.gather_userlists()

user_dropdown = dcc.Dropdown(options=sorted(uid_list),
                            value='s4595555')

user_table = dash_table.DataTable()

app.layout = html.Div(children=[
    html.H1(children='User dashboard'),
    user_dropdown,
    dbc.Badge("Project", id='badge-proj', color="Success",className="ms-1"),
    dash_table.DataTable(id='project-table', style_as_list_view=True,),    
    ])


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



if __name__ == '__main__':
    app.run_server(debug=True)











def entry_main():
    app.run_server(debug=False)

if __name__ == '__main__':
    app.run_server(debug=True)