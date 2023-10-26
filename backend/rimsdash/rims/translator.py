



def projectsv2(project):
    """
    'Project ID': ,
    'Title': "",
    'Project type': '',
    'Main group': '',
    'Email of the supervisor': '',
    'Project requested by user name': '',
    'Project requested by user email': '',
    'Participant Users': '',
    'Participant Groups': ' ',
    'Visibility': '',
    'Account number': '',
    'Email of budget holder': '',
    'Expiration date': '',
    'Affiliation': '',
    'Phase': ,
    'Status': '',
    'Active': ,
    'Edu person principal name': '',
    'Sub org unit': '',
    'UQRDM Collection #': ''},
    """

    result = {}

    result['id'] = int(project['Project ID'])
    result['title'] = str(project['Title'])
    result['type'] = str(project['Project type'])
    result['phase'] = str(project['Phase'])
    result['description'] = ''  #not present
    result['qcollection'] = str(project['UQRDM Collection #'])
    result['coreid'] = None
    result['active'] = str(project['Active'])

    return result


