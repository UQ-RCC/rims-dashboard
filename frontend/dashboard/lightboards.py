import sys, os
from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
import dash_daq as daq

class ColourList():
    def __init__(self):
        #base
        self.off = "#BBBBBB"
        #good
        self.work = "#77ffaa"
        self.ok = "#33f975"
        self.active = "#33f9f9"
        #bad
        self.warn = "#ffb34d"
        self.fail = "#fc5959"
        self.na = "#ffffff"



COLOURLIST = ColourList()


BRAND_COLOURS={'purple':(81,36,122), 'lpurple':(150,42,139),'red':(230,38,69), 'blue':(64,133,198), \
            'aqua':(0,162,199), 'grey':(215,209,204), "dgrey":(153,148,144), \
            'gold':(217,172,109), 'green':(46,168,54), 'orange':(235,96,43),\
            'yellow':(251,184,0), 'black':(0,0,0), 'white':(255,255,255) }

#TODO: request this from backend as dict to avoid disconnecting in future
class IState():
    def __init__(self):
        #base
        self.off = 0
        #good
        self.work = 1
        self.ok = 2
        self.active = 3
        #bad
        self.warn = 11
        self.fail = 12
        self.na = -1

ISTATES = IState()


def colour_from_istate(state: int):
    if state == ISTATES.off:
        return COLOURLIST.off
    elif state == ISTATES.work:
        return COLOURLIST.work
    elif state == ISTATES.ok:
        return COLOURLIST.ok
    elif state == ISTATES.active:
        return COLOURLIST.active
    elif state == ISTATES.warn:
        return COLOURLIST.warn
    elif state == ISTATES.fail:
        return COLOURLIST.fail
    elif state == ISTATES.na:
        return COLOURLIST.na
    else:
        raise ValueError("unknown value for state: {state}")


def create_lightcell(title, name, size=30):
    return html.Div([
            html.H6(f"{title}", style={'text-align': 'center', 'align': 'center'}),
            daq.Indicator(
                id=f"{name}",
                label="",
                size=size,
                color=COLOURLIST.off,
                className='indicator',
                value='False',
                ),
            ], className='lightcell',
    )

def create_lightcell_small(name, number, size=22):
    return html.Div([
            daq.Indicator(
                id=f"{name}-{number}",
                label="",
                size=size,
                color=COLOURLIST.off,
                className='indicator-small',
                value='False',                
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
                    html.H6(f"Project", className="rowlabel"),      #TO-DO project # here
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





