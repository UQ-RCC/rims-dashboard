import sys, os
from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
import dash_daq as daq

class ColorList():
    def __init__(self):
        self.success = "#33f975"
        self.warn = "#ffb34d"
        self.fail = "#fc5959"
        self.wait = "#77ffaa"
        self.neutral = "#BBBBBB"
        self.white = "#ffffff"

colorlist = ColorList()



def create_lightcell(title, name, size=30):
    html.Div(
        [
            html.H6(f"title"),
            daq.Indicator(
                id='name',
                label="",
                size=size,
                color=colorlist.neutral,
            ),            
        ], align="center"
    )


primary_dash=html.Div(
    [
        dbc.Row(
            [
                dbc.Col([
                    html.H6("User"),
                    daq.Indicator(
                        id='ind-prim-user',
                        label="",
                        size=30,
                        color=colorlist.neutral,
                    )],
                    width={ 'size': 1, 'offset': 1},
                    align="center",
                ),
                dbc.Col([
                    html.H6("Project"),
                    daq.Indicator(
                        id='ind-prim-proj',
                        label="",
                        size=30,
                        color=colorlist.neutral,
                        style={}
                    )],
                    width={ 'size': 1, 'offset': 0},
                    align="center",
                ),
            ],
            align="center",
        ) 
    ])


rights_dash=html.Div(
    [
        dbc.Row(
            [
                dbc.Col([
                    html.H6("Hawken"),
                    daq.Indicator(
                        id='ind-acc-hawk',
                        label="",
                        size=30,
                        color=colorlist.neutral,
                        style={}
                    )], 
                    width={ 'size': 1, 'offset': 1},
                    align="center",
                ),
                dbc.Col([
                    html.H6("AIBN"),
                    daq.Indicator(
                        id='ind-acc-aibn',
                        label="",
                        size=30,
                        color=colorlist.neutral,
                        style={}
                    )], 
                    width={ 'size': 1, 'offset': 0},
                    align="center",
                ),
                dbc.Col([
                    html.H6("Chemistry"),
                    daq.Indicator(
                        id='ind-acc-chem',
                        label="",
                        size=30,
                        color=colorlist.neutral,
                        style={}
                    )], 
                    width={ 'size': 1, 'offset': 0},
                    align="center",
                ),        
                dbc.Col([
                    html.H6("QBP"),
                    daq.Indicator(
                        id='ind-acc-qbp',
                        label="",
                        size=30,
                        color=colorlist.neutral,
                        style={}
                    )], 
                    width={ 'size': 1, 'offset': 0},
                    align="center",
                ),        
            ],
            align="center",
        )
    ]
)


project_dash=html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    daq.Indicator(
                        id='ind-proj-active',
                        label="Active",
                        size=30,
                        color=colorlist.neutral,
                        style={}
                    )
                ),
                dbc.Col(
                    daq.Indicator(
                        id='ind-proj-p0',
                        label="0",
                        size=15,
                        color=colorlist.neutral,
                        style={}
                    )
                ),
                dbc.Col(
                    daq.Indicator(
                        id='ind-proj-p1',
                        label="1",
                        size=15,
                        color=colorlist.neutral,
                        style={}
                    )
                ),
                dbc.Col(
                    daq.Indicator(
                        id='ind-proj-p2',
                        label="1",
                        size=15,
                        color=colorlist.neutral,
                        style={}
                    )
                ),
                dbc.Col(
                    daq.Indicator(
                        id='ind-proj-p3',
                        label="3",
                        size=15,
                        color=colorlist.neutral,
                        style={}
                    )
                ),                
                dbc.Col(
                    daq.Indicator(
                        id='ind-proj-acc',
                        label="Billing",
                        size=30,
                        color=colorlist.neutral,
                        style={}
                    )
                ),        
                dbc.Col(
                    daq.Indicator(
                        id='ind-proj-ohs',
                        label="Risk assessment",
                        size=30,
                        color=colorlist.neutral,
                        style={}
                    )
                ),      
                dbc.Col(
                    daq.Indicator(
                        id='ind-proj-rdm',
                        label="Data storage",
                        size=30,
                        color=colorlist.neutral,
                        style={}
                    )
                ),   
            ],
            align="center",        
        )
    ]
)





