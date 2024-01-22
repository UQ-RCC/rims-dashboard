import logging
import uvicorn
import os 

from fastapi import FastAPI, Depends    #, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from logging.handlers import TimedRotatingFileHandler

import rimsdash.config as config
import rimsdash.utils.keycloak as keycloak

#from rimsdash.routers import general
from rimsdash.routers import navbar, projects, sync, training_requests


#logging setup
log_level = logging.DEBUG

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
    prefix="/rapi/v1",
    tags=['navbar'],
    dependencies=[Depends(keycloak.decode)],    
    responses={404: {"description": "Not found"}},
)

app.include_router(
    projects.router,
    prefix="/rapi/v1",
    tags=['projects'],
    dependencies=[Depends(keycloak.decode)],    
    responses={404: {"description": "Not found"}},
)

app.include_router(
    training_requests.router,
    prefix="/rapi/v1",
    tags=['trainingrequests'],
    dependencies=[Depends(keycloak.decode)],
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


logger.info("App started")

#Dev mode
def entry_dev():
    logger.info("Starting app as dev")
    uvicorn.run(app, host="127.0.0.1", port=5000)
    logger.info("App started as dev")

if __name__ == "__main__":
    entry_dev()