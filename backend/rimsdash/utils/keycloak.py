from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak.realm import KeycloakRealm
from keycloak.openid_connect import KeycloakOpenidConnect
from fastapi import Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR
from jose.exceptions import ExpiredSignatureError

from rimsdash import config

realm = KeycloakRealm(
    server_url=config.get('keycloak', 'server_url'), 
    realm_name=config.get('keycloak', 'realm_name')
)

keycloak_openid = KeycloakOpenidConnect(
    realm=realm, 
    client_id=config.get('keycloak', 'client_id'),
    client_secret=config.get('keycloak', 'client_secret')
)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=config.get('keycloak', 'authorization_url'),
    tokenUrl=config.get('keycloak', 'token_url'),
)

"""
Decode the token
"""
def decode(token: str = Depends(oauth2_scheme)):
    KEYCLOAK_PUBLIC_KEY = (
        "-----BEGIN PUBLIC KEY-----\n"
        + config.get('keycloak', 'public_key')
        + "\n-----END PUBLIC KEY-----"
    )
    try:
        return keycloak_openid.decode_token(
            token,
            key=KEYCLOAK_PUBLIC_KEY,
            options={"verify_signature": True, "verify_aud": False, "exp": True},
        )
    except ExpiredSignatureError as e:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Token expired.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{str(e)}",
        )
