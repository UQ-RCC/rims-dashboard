    
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

router = APIRouter()
logger = logging.getLogger('rimsdash')

ACCEPTED_REALMS = {'admin', 'dashboard'}

OK_RESPONSE = JSONResponse(status_code=200, content={"message": "keycloak OK"})

FALLBACK_ERROR = JSONResponse(status_code=400, content={"message": "request not completed, unspecified error during authentication"})


def lookup_admin_rights(db: Session, keycloak_user: dict) -> bool:
    """
    extracts user from decoded keycloak token and checks their access

    Any failure needs to raise exception
    """

    try:
        email = keycloak_user.get('email')
        realm_access = keycloak_user.get('realm_access')
    except:
        raise Exception(f"Could not extract user from keycloak token")

    #if the keycloak token has the appropriate realm (eg. admin), return ok
    if realm_access and \
        any ( realm in ACCEPTED_REALMS for realm in realm_access.get('roles') ):
        return True
    
    #if the email exists, look it up and return its admin status in DB
    elif email is None:
        raise Exception(f"No user email id present in keycloak token")
    else:
        logger.debug(f"User email is |{email}|")
        user = crud.user.get_by_email(db, email)
        
        if not user:
            raise Exception(f"Email {email} from keycloak token not found in DB")

        elif user.admin == False:
            raise Exception(f"Access denied for {user.username} {email}, admin={user.admin}")

        elif user.admin == True:
            logger.debug(f"Keycloak ok for {user.username} {email}")
            return True
        else:
            raise Exception(f"Unspecified error parsing keycloak token")

def lookup_user(db: Session, keycloak_user: dict) -> bool:
    """
    extracts user from decoded keycloak token and checks their access
    
    if admin = False, returns false instead of raising exception
    """

    try:
        email = keycloak_user.get('email')
        logger.info(f"User email is |{email}|")
        realm_access = keycloak_user.get('realm_access')
        logger.info(f"User realm is |{realm_access}|")
        logger.info(f"Error on email fetch, token content is |{keycloak_user}|")
        logger.info(f"session is |{db}|")
    except:
        raise Exception(f"Could not extract user from keycloak token")

    #if the keycloak token has the appropriate realm (eg. admin), return ok
    if realm_access and \
        any ( realm in ACCEPTED_REALMS for realm in realm_access.get('roles') ):
        return True
    
    #if the email exists, look it up and return its admin status in DB
    elif email is None:
        raise Exception(f"No user email id present in keycloak token")
    else:
        try:
            user = crud.user.get_by_email(db, email)
        except:
            raise Exception(f"Error searching for {email} in DB")

        if not user:
            raise Exception(f"Email {email} from keycloak token not found in DB")

        elif user.admin == False:
            logger.info(f"Keycloak denied for {user.username} {email}, {user.admin == False}")
            return False

        elif user.admin == True:
            logger.debug(f"Keycloak ok for {user.username} {email}")
            return True
        else:
            raise Exception(f"Unspecified error parsing keycloak token")        