import logging
import sys

from fastapi import APIRouter, Depends, HTTPException, status
#import rimsdash.db as rdb
#from sqlalchemy.orm import Session

import rimsdash.usergather as gather
import rimsdash.external as external
import rimsdash.service as service

router = APIRouter()
logger = logging.getLogger('rimsdash')


"""
#DB and keycloak example from pitschi-xapi:
@router.get("/collections")
async def get_collections(db: Session = Depends(rdb.get_db)):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorised"
        )
    else: 
        realm_access = user.get('realm_access')
        has_dashboard_access = realm_access and 'dashboard' in realm_access.get('roles')
        if not has_dashboard_access:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorised. Only dashboard can do this."
            )
        return pdb.crud.get_collections(db)
"""

@router.get("/userlist")
async def api_getuserlist():
    userlist=service.populate_userdropdown()

    return userlist


@router.get("/userprojects")
async def api_getuserprojects(login: str):
    
    user_projects = external.get_user_projects(login)
    
    return user_projects

@router.get("/projectdetails")
async def api_getprojectdetails(project_number: int):    #expects project_number
  
    #here we create a df from a json then convert back to dict-list after
    #should just drop the df intermediary
    project_info_df = gather.gather_projectdetails(project_number)
    
    project_info = project_info_df.to_dict('records')

    return project_info


@router.get("/userstate")
async def api_getuserstate(login: str): #expects user_login
       
    result = service.get_user_indicators(login)  #dict
    
    return result
  


@router.get("/allprojectstates")
async def api_getallprojectstates(): 

    result = service.get_all_project_states()  #list of dicts

    return result


@router.get("/userprojectstates")
async def api_getuserprojectstates(login: str): #expects user_login

    result = service.get_user_project_indicators(login)  #dict

    return result

@router.get("/defaultuserstate")
async def api_defaultuserstate():

    result = service.get_default_user_indicator()  #dict

    return result
    

@router.get("/defaultuserprojectstates")
async def api_defaultprojectstates():

    result = [ service.get_default_project_indicator() ] #dict
   
    return result

@router.get("/defaultprojectstate")
async def api_defaultprojectstate():
    result = service.get_default_project_indicator()  #dict

    return result

@router.get("/userfromemail")
async def api_userbyemail(email: str): #expects email
    
    result = service.user_from_email(email)  #dict

    return result

@router.get("/checkadminbyemail")
async def api_adminstatusbyemail(email: str): #expects email

    _login = service.user_from_email(email)['login']
    result = service.admin_status(_login)  #dict

    return result




