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



def sort_paired(list1, list2):
    zipped = zip(list1, list2)           
    result1, result2 = zip(*sorted(zipped))
    return result1, result2



def iid_colour(value: int):
    if value == 0:
        result = "#BBBBBB"
    elif value == 1:
        result = "#77ffaa"       
    elif value == 2:
        result = "#33f975"  
    elif value == 3:
        result = "#3375f9"  
    elif value == 11:
        result = "#ffb34d"    
    elif value == 12:
        result = "#fc5959"      
    elif value == -1:
        result = "#ffffff"       
    else:
        raise ValueError(f"invalid value for {value}")

    return result

def iid_str(value: int):
    if value == 0:
        result = "neutral"
    elif value == 1:
        result = "progress"        
    elif value == 2:
        result = "success"    
    elif value == 3:
        result = "full"             
    elif value == 11:
        result = "warn"       
    elif value == 12:
        result = "fail"       
    elif value == -1:
        result = "na"       
    else:
        raise ValueError(f"invalid value for {value}")

    return result