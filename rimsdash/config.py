"""
Adapted from https://github.com/UQ-RCC/pitschi-xapi
c. 2021, The University of Queensland
Apache 2.0 
"""

import configparser
import os
import errno

config = configparser.ConfigParser()
config.read(["conf/rimsdash.conf", os.environ.get("RIMSDASH_CONFIG", "")])

def get(section, option, default = None, required=False):
    """
    Reads config optoin from the given section, returning default if not found
    """
    try:
        return config.get(section, option).strip()
    except:
        if required: 
            raise Exception(f"option {option} is required in section {section}")
        else:
            return default