import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import rimsdash.external as external
import rimsdash.config as config


UQ_COLOURS={'purple':(81,36,122), 'lpurple':(150,42,139),'red':(230,38,69), 'blue':(64,133,198), \
            'aqua':(0,162,199), 'grey':(215,209,204), "dgrey":(153,148,144), \
            'gold':(217,172,109), 'green':(46,168,54), 'orange':(235,96,43),\
            'yellow':(251,184,0), 'black':(0,0,0), 'white':(255,255,255) }

Y_CUTOFF = int(config.get('visualisation','min_hours', default=100))


def usage_bar(usage):
    """
    simple bar chart in UQ branded colours, stacked by source
    """
    layout = go.Layout(
        paper_bgcolor='rgba(255,255,255,125)',
        plot_bgcolor='rgba(255,255,255,125)'
    )

    fig = go.Figure(data=[
        go.Bar(name='User', x=usage['date'], y=usage['user_hours'], marker=dict(color = f"rgb{UQ_COLOURS['purple']}")),
        go.Bar(name='Internal', x=usage['date'], y=usage['internal_hours'], marker=dict(color = f"rgb{UQ_COLOURS['lpurple']}"))
    ], layout=layout)

    if max(usage['user_hours']+usage['internal_hours']) < Y_CUTOFF:
        fig.update_yaxes(range=[0, Y_CUTOFF])
    
    # Change the bar mode
    fig.update_layout(barmode='stack')
    #fig.show()

    return fig