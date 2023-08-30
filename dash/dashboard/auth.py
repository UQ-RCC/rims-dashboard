import dashboard.config as config

DEFAULT_VALUE = 'xxxxxx'

def get_auth_details():

    username = config.get('authentication', 'username')
    password = config.get('authentication', 'password')

    if username == "DEFAULT_VALUE":
        raise ValueError("example username still present, you must change this to start the app")

    if password == "DEFAULT_VALUE":    
        raise ValueError("example password still present, you must change this to start the app")

    result = { username: password }

    return result