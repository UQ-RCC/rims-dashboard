import os, sys
import logging
import uvicorn

from fastapi import FastAPI, Depends    #, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from logging.handlers import TimedRotatingFileHandler

import rimsdash.config as config
import rimsdash.utils.keycloak as keycloak

#from rimsdash.routers import general
from rimsdash.routers import unsecured, navbar, projects, sync, training_requests


#logging setup
log_level_in: str = config.get('logging', 'log_level')

#set log level from config
if "debug" in log_level_in.lower():
    log_level = logging.DEBUG
elif "info" in log_level_in.lower():
    log_level = logging.INFO
elif "warn" in log_level_in.lower():
    log_level = logging.WARN
elif "error" in log_level_in.lower():
    log_level = logging.ERROR
else:
    #default info
    log_level = logging.INFO

logger = logging.getLogger('rimsdash')

logger.setLevel(log_level)

log_file = config.get('logging', 'log_file', default = "/var/log/rimsdash/rimsdash.log")

#   create the directory if it is missing
os.makedirs(os.path.dirname(log_file), exist_ok=True)

#filehandler
fh = TimedRotatingFileHandler(log_file, when='midnight',backupCount=7)
fh.setLevel(log_level)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

#add handlers
logger.addHandler(fh)
logging.getLogger("uvicorn.access").addHandler(fh)
logging.getLogger("uvicorn.error").addHandler(fh)
logging.getLogger("uvicorn").addHandler(fh)

#streamhandler
sh = logging.StreamHandler(sys.stderr)  # Use sys.stderr for stderr
sh.setLevel(log_level)
sh.setFormatter(formatter)

#add handlers
logger.addHandler(sh)
logging.getLogger("uvicorn.access").addHandler(sh)
logging.getLogger("uvicorn.error").addHandler(sh)
logging.getLogger("uvicorn").addHandler(sh)



#App setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#api routers

app.include_router(
    navbar.router,
    prefix="/rims/api/v1",
    tags=['navbar'],
    dependencies=[Depends(keycloak.decode)],    
    responses={404: {"description": "Not found"}},
)

app.include_router(
    projects.router,
    prefix="/rims/api/v1",
    tags=['projects'],
    dependencies=[Depends(keycloak.decode)],    
    responses={404: {"description": "Not found"}},
)

app.include_router(
    training_requests.router,
    prefix="/rims/api/v1",
    tags=['trainingrequests'],
    dependencies=[Depends(keycloak.decode)],
    responses={404: {"description": "Not found"}},
)

#IMPORANT: unsecured, use for ready ping only
app.include_router(
    unsecured.router,
    prefix="/rims/api/v1",
    tags=['open'],   
    responses={404: {"description": "Not found"}},
)


# automatic tasks
if (bool(config.get('sync', 'automatic_sync', default = False)) == True):
    logger.info("Automatic syncing on")
    app.include_router(
        sync.router
    )
else:
    logger.info("Automatic syncing off")

#Dev mode
def entry_dev():
    logger.info("App starting in dev")
    logger.info(f"logging initiated at level: {logger.level}, {log_level_in}")
    uvicorn.run(app, host="127.0.0.1", port=80) 

if __name__ == "__main__":
    entry_dev()