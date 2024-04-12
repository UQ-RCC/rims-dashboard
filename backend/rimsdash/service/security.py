    
import logging
import sys

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

import rimsdash.config as config
import rimsdash.db as rdb
import rimsdash.crud as crud
import rimsdash.schemas as schemas
import rimsdash.utils.keycloak as keycloak
import rimsdash.service as service

from rimsdash.models import AdminRight

router = APIRouter()
logger = logging.getLogger('rimsdash')

USE_REALM =(config.get('access_control', 'use_realm', default = True) == "True")    #string to bool
ALLOWED_REALMS = config.get_csv_list('access_control', 'allowed_realms', default = [] )

OK_RESPONSE = JSONResponse(status_code=200, content={"message": "keycloak OK"})

FALLBACK_ERROR = JSONResponse(status_code=400, content={"message": "request not completed, unspecified error during authentication"})


def lookup_admin_rights(db: Session, keycloak_user: dict) -> bool:
    """
    extracts user from decoded keycloak token and checks their access

    returns True if user has admin/realm access, otherwise raises exception

    """

    try:
        email = keycloak_user.get('email')
        logger.debug(f"Querying access for |{email}|")
        realm_access = keycloak_user.get('realm_access')
    except:
        raise Exception(f"Could not extract user from keycloak token")

    #if the keycloak token has the appropriate realm (eg. admin), return ok
    if USE_REALM and realm_access is not None and \
        any ( realm in ALLOWED_REALMS for realm in realm_access.get('roles') ):
        logger.debug(f"Keycloak accepted by realm for {email}, {realm_access}")
        return True
    
    #if the email does not exist, return error
    elif email is None:
        raise Exception(f"No user email id present in keycloak token")
    
    #else check RIMS access using email in token
    else:
        try:
            user = crud.user.get_by_email(db, email=email)
        except:
            raise Exception(f"Error fetching {email} in DB")

        if not user:
            raise Exception(f"Email {email} from keycloak token not found in DB")

        elif not user.admin == AdminRight.admin:
            raise Exception(f"Access denied for non-admin user {user.username} {email}, admin={user.admin}")

        elif user.admin == AdminRight.admin:
            logger.debug(f"RIMS access OK for {user.username} {email}")
            return True
        else:
            raise Exception(f"Unspecified error parsing keycloak token")  


def lookup_user(db: Session, keycloak_user: dict) -> bool:
    """
    extracts user from decoded keycloak token and checks their access
    
    returns True if user has admin/realm access, otherwise returns False

    """
    
    try:
        email = keycloak_user.get('email')
        logger.debug(f"Querying access for {email}")
        realm_access = keycloak_user.get('realm_access')
    except:
        raise Exception(f"Could not extract user from keycloak token")

    #if we are using realms, and token has appropriate realm, return ok

    if USE_REALM and realm_access is not None and \
        any ( realm in ALLOWED_REALMS for realm in realm_access.get('roles') ):
        logger.debug(f"Access accepted by realm for {email}, {realm_access}")
        return True

    #if the email does not exist, return error
    elif email is None:
        raise Exception(f"No user email id present in keycloak token")
    
    #else check RIMS access using email in token
    else:
        try:
            user = crud.user.get_by_email(db, email=email)
        except:
            raise Exception(f"Error fetching {email} in DB")

        if not user:
            raise Exception(f"Email {email} from keycloak token not found in DB")

        elif not user.admin == AdminRight.admin:
            logger.debug(f"Unpriveleged access for {user.username} {email}, admin={user.admin}")
            return False

        elif user.admin == AdminRight.admin:
            logger.debug(f"RIMS access OK for {user.username} {email}")
            return True
        else:
            raise Exception(f"Unspecified error parsing keycloak token")        
    

def lookup_realm_rights(db: Session, keycloak_user: dict) -> bool:
    """
    extracts user from decoded keycloak token and checks their access

    returns True if user has admin/realm access, otherwise raises exception

    """

    try:
        email = keycloak_user.get('email')
        logger.debug(f"Querying access for |{email}|")
        realm_access = keycloak_user.get('realm_access')
    except:
        raise Exception(f"Could not extract user from keycloak token")

    #if the keycloak token has the appropriate realm (eg. admin), return ok
    if USE_REALM and realm_access is not None and \
        any ( realm in ALLOWED_REALMS for realm in realm_access.get('roles') ):
        logger.debug(f"Keycloak accepted by realm for {email}, {realm_access}")
        return True
    else:
        raise Exception(f"Superuser access denied for user {email}, realms {realm_access.get('roles')} not accepted" )