import sys, os
from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
import dash_daq as daq

import rimsdash.collate as collate

class ColorList():
    def __init__(self):
        #base
        self.off = "#BBBBBB"
        #good
        self.work = "#77ffaa"
        self.on = "#33f975"
        self.full = "#3375f9"
        #bad
        self.warn = "#ffb34d"
        self.fail = "#fc5959"
        self.na = "#ffffff"

COLORLIST = ColorList()

def color_from_istate(state: int):
    if state == collate.istate.off:
        return COLORLIST.off
    elif state == collate.istate.work:
        return COLORLIST.work
    elif state == collate.istate.on:
        return COLORLIST.on
    elif state == collate.istate.full:
        return COLORLIST.full
    elif state == collate.istate.warn:
        return COLORLIST.warn
    elif state == collate.istate.fail:
        return COLORLIST.fail
    elif state == collate.istate.na:
        return COLORLIST.na
    else:
        raise ValueError("unknown value for state: {state}")


def create_lightcell(title, name, size=30):
    return html.Div([
            html.H6(f"{title}", style={'text-align': 'center', 'align': 'center'}),
            daq.Indicator(
                id=f"{name}",
                label="",
                size=size,
                color=COLORLIST.off,
                className='indicator',
                ),
            ], className='lightcell',
    )

def create_lightcell_small(name, number, size=22):
    return html.Div([
            daq.Indicator(
                id=f"{name}_p{number}",
                label="",
                size=size,
                color=COLORLIST.off,
                className='indicator-small',
                ),
            html.P(f"{number}", className='text-indicator-small')                
            ], className='lightcell-small',
    )    

def create_phasecell(name):
    return html.Div(
        [
            html.H6(f"Phase", style={'text-align': 'center',}),
            html.Div(
            [
                create_lightcell_small(name, 0),            
                create_lightcell_small(name, 1),
                create_lightcell_small(name, 2),
                create_lightcell_small(name, 3),
            ], style={'padding-left': '0px'}),
        ], className='phasecell'
    )    


primary_dash=html.Div(
    [
        dbc.Row(),
        dbc.Row(
            [
                dbc.Col([
                    html.H6('Core:', className="grouplabel"),
                    ], 
                    width={'size': 1, 'offset': 0},
                    className="lightcol",
                ),                 
                dbc.Col([
                        create_lightcell("User", 'ind-prim-user'),
                    ],
                    width={'size': 1, 'offset': 0},
                    className="lightcol",
                ),
                dbc.Col([
                        create_lightcell("Project", 'ind-prim-proj'),
                    ],
                    width={'size': 1, 'offset': 0},
                    className="lightcol",
                ),
            ],
            className="lightrow",
        ) 
    ],
    className="lightgroup", 
)


rights_dash=html.Div(
    [
        dbc.Row(),
        dbc.Row(
            [
                dbc.Col([
                    html.H6('Access:', className="grouplabel"),
                    ], 
                    width={'size': 1, 'offset': 0},
                    className="lightcol",
                ),                  
                dbc.Col([
                    create_lightcell("Hawken", 'ind-acc-hawk', 30),
                    ], 
                    width={'size': 1, 'offset': 0},
                    className="lightcol",
                ),
                dbc.Col([
                    create_lightcell("AIBN", 'ind-acc-aibn', 30),
                    ], 
                    width={'size': 1, 'offset': 0},
                    className="lightcol",
                ),
                dbc.Col([
                    create_lightcell("Chemistry", 'ind-acc-chem', 30),
                    ], 
                    width={'size': 1, 'offset': 0},
                    className="lightcol",
                ),        
                dbc.Col([
                    create_lightcell("QBP", 'ind-acc-qbp', 30),
                    ], 
                    width={'size': 1, 'offset': 0},
                    className="lightcol",
                ),        
            ],
            className="lightrow",
        )
    ],
    className="lightgroup"
)


project_dash=html.Div(
    [
        dbc.Row(),
        dbc.Row(
            [
                dbc.Col([
                    html.H6(f"P#1125", className="rowlabel"),
                    ], 
                    width={'size': 1, 'offset': 0},
                    className="lightcol",
                ),                
                dbc.Col([
                    create_lightcell("Active", 'ind-proj-active', 30),
                    ], 
                    width={'size': 1, 'offset': 0},
                    className="lightcol",
                ),
                dbc.Col([
                    create_lightcell("Billing", 'ind-proj-acc', 30),
                    ], 
                    width={'size': 1, 'offset': 0},
                    className="lightcol",
                ),        
                dbc.Col([
                    create_lightcell("RA", 'ind-proj-ohs', 30),
                    ], 
                    width={'size': 1, 'offset': 0},
                    className="lightcol",
                ),   
                dbc.Col([
                    create_lightcell("RDM", 'ind-proj-rdm', 30),
                    ], 
                    width={'size': 1, 'offset': 0},
                    className="lightcol",
                ),                  
                dbc.Col([
                    create_phasecell('ind-proj-phase'),
                    ], 
                    width={'size': 3, 'offset': 0},
                    className="phasecol",
                ),      
           ],
            className="lightrow",       
        )
    ],
    className="lightgroup",
)





