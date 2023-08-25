import json
import requests
import dashboard.config as config

BACKEND_URL=f"{config.get('backend','url')}"
BACKEND_PORT=f"{config.get('backend','port')}"

def getuserlist():
    """
    """    
    url=f"{BACKEND_URL}"
    port=f"{BACKEND_PORT}"
    route=f"/api/v1/userlist"

    response = requests.request("GET", f"{url}:{port}{route}")

    if response.ok:
        if response.status_code == 204:
            raise Exception('Not found')
        else:
            return response.json(strict=False)
    else:
        raise Exception('Not found')


def getstate():
    """
    """    
    url=f"{BACKEND_URL}"
    port=f"{BACKEND_PORT}"
    route=f"/api/v1/getstate"

    response = requests.request("GET", f"{url}:{port}{route}")

    if response.ok:
        if response.status_code == 204:
            raise Exception('Not found')
        else:
            return response.json(strict=False)
    else:
        raise Exception('Not found')


#TODO pass arg in request 
def getuserprojects(user_login):
    """
    """    
    url=f"{BACKEND_URL}"
    port=f"{BACKEND_PORT}"
    route=f"/api/v1/getstate"

    response = requests.request("GET", f"{url}:{port}{route}")

    if response.ok:
        if response.status_code == 204:
            raise Exception('Not found')
        else:
            return response.json(strict=False)
    else:
        raise Exception('Not found')
    

def getprojectdetails(project_num):
    """
    """    
    url=f"{BACKEND_URL}"
    port=f"{BACKEND_PORT}"
    route=f"/api/v1/getstate"

    response = requests.request("GET", f"{url}:{port}{route}")

    if response.ok:
        if response.status_code == 204:
            raise Exception('Not found')
        else:
            return response.json(strict=False)
    else:
        raise Exception('Not found')