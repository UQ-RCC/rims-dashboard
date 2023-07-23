import plotly

def df_display(df):
    import plotly.graph_objs as go
    fig = go.Figure(data=[go.Table(
    header=dict(values=list(df.columns),
                align='left'),
    cells=dict(values=[df[i] for i in df.columns],           
                align='left'))
    ])
    return fig


def safecast_int(input: str):
    """
    attempts to cast input str to int
    
    if fails, returns -1
    """    
    try:
        result = int(input)
    except:
        result = -1
    finally:
        return result