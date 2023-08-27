import json
import requests
import dashboard.config as config

BACKEND_URL=f"{config.get('backend','url')}"
BACKEND_PORT=f"{config.get('backend','port')}"


def get_response(url:str, port:str, route:str, payload:str=''):
    if payload == '':
        response = requests.request("GET", f"{url}:{port}{route}")
    else:
        response = requests.request("GET", f"{url}:{port}{route}", params=payload)

    if response.ok:
        if response.status_code == 204:
            raise Exception('Not found')
        else:
            return response.json(strict=False)
    else:
        raise Exception(f'API response not ok, status code: {response.status_code}')    

def get_user_list():
    """
    """    
    url=f"{BACKEND_URL}"
    port=f"{BACKEND_PORT}"
    route=f"/api/v1/userlist"

    return get_response(url, port, route)


def get_state(user_login):
    """
    """    
    route=f"/api/v1/getstate"
    url=f"{BACKEND_URL}"
    port=f"{BACKEND_PORT}"
    payload=f"login={user_login}"

    return get_response(url, port, route, payload=payload)


#TODO pass arg in request 
def get_user_projects(user_login):
    """
    """    
    route=f"/api/v1/getuserprojects"
    url=f"{BACKEND_URL}"
    port=f"{BACKEND_PORT}"
    payload=f"login={user_login}"

    return get_response(url, port, route, payload=payload)
    

def get_project_details(project_number):
    """
    """    
    url=f"{BACKEND_URL}"
    port=f"{BACKEND_PORT}"
    route=f"/api/v1/getprojectdetails"
    payload=f"project_number={project_number}"

    return get_response(url, port, route, payload=payload)