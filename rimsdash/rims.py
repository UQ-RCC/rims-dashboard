"""
Adapted from https://github.com/UQ-RCC/pitschi-xapi
c. 2021, The University of Queensland 
Apache 2.0
"""

import json, csv
import requests
import datetime
import logging
import rimsdash.config as config


logger = logging.getLogger('pitschixapi')


def get_usage_per_project(start_date=datetime.date(2022, 7, 1), end_date=datetime.date(2022, 7, 31)):
    """
    requests instrument usage per project between start and end dates from RIMS API
    returns as json
    """    
    date_format='%Y-%m-%d'
    report_no=1064
    url=f"{config.get('ppms','ppms_url')}API2/"
    key=f"{config.get('ppms', 'api2_key')}"
    return_format=f"json"
    payload=f"apikey={key}&action=Report{report_no}&startDate={start_date.strftime(date_format)}&endDate={end_date.strftime(date_format)}&dateformat=print&outformat={return_format}&coreid=2"
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.ok:
        if response.status_code == 204:
            raise Exception('Not found')
        else:
            return response.json(strict=False)
    else:
        raise Exception('Not found')


def get_systems():
    logger.debug("Querying systems")
    url = f"{config.get('ppms', 'ppms_url')}pumapi/"
    payload=f"apikey={config.get('ppms', 'ppms_key')}&action=getsystems"
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.ok:
        if response.status_code == 204:
            return {}
        else:
            # format is in csv
            _systems_text = response.text
            _csv_reader = csv.reader(_systems_text.split('\n'), delimiter=',')
            _csv_reader.__next__()
            systems = {}
            for row in _csv_reader:
                if(len(row) > 3):
                    _systemid = int(row[1])
                    _systemtype = row[2]
                    _systemname = row[3]
                    systems[_systemname] = {'systemid': _systemid, 'systemtype': _systemtype, 'systemname': _systemname}
            return systems
    return {}