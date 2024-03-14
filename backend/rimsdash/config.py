"""
Adapted from https://github.com/UQ-RCC/pitschi-xapi
c. 2021, The University of Queensland
Apache 2.0 
"""

import configparser
import os
import errno
BASE_DIR=os.path.dirname(os.path.realpath(os.path.dirname(__file__)))


config = configparser.ConfigParser()
config.read([os.path.join(BASE_DIR,"conf/rimsdash.conf"), os.environ.get("rimsdash_CONFIG", "")])

def get(section: str, option: str, default = None, os_env=True, required=False):
    """
    Reads config option from the given section, returning default if not found
    """
    cp_vars = os.environ if os_env else None
    try:
        return config.get(section, option, vars=cp_vars).strip()
    except:
        if required: 
            raise Exception(f"Required config field {option} not found in section {section}")
        else:
            return default


def get_csv_list(section: str, option: str, required=False, default=None):
    """
    Tidies up a csv list
    """    
    try:
        string_list = get(section, option, required=required, default=default)
        string_list=string_list.replace(' ', '')
        string_list=string_list.split(',')
        return string_list        
    except:
        if required:
            raise Exception(f"Error reading csv list from config, {option} not found in section {section}")            
        else:
            return default