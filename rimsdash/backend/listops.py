
from numbers import Number


"""
Functions for searching simple json list-of-dict objects returned by RIMS API
"""

def search_substring(dict_list, field: str, target: str ):
    return list(filter(lambda result: f'{target}' in result[f'{field}'], dict_list))

def search_string(dict_list, field: str, target ):
    return list(filter(lambda result: result[f'{field}'] == f'{target}', dict_list))

def search_value(dict_list, field: str, target: Number ):
    return list(filter(lambda result: result[f'{field}'] == target, dict_list))



#objectpath is worth looking at as more functional alternative
#http://objectpath.org/
#https://stackoverflow.com/questions/8383136/parsing-json-and-searching-through-it