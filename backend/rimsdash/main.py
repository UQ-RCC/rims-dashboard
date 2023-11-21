import logging
import uvicorn
import os 

from fastapi import FastAPI #, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from logging.handlers import TimedRotatingFileHandler

#from rimsdash.routers import general
from rimsdash.routers import navbar
from rimsdash.routers import projects
import rimsdash.config as config


#logging setup
logger = logging.getLogger('rimsdash')
logger.setLevel(logging.DEBUG)

log_file = config.get('logging', 'log_file', default = "/var/log/rimsdash/rimsdash.log")
#   create the directory if it is missing
os.makedirs(os.path.dirname(log_file), exist_ok=True)
fh = TimedRotatingFileHandler(log_file, when='midnight',backupCount=7)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
logging.getLogger("uvicorn.access").addHandler(fh)
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

#app.include_router(
#    general.router,
#    prefix="/rapi/v1",
#    tags=['general'],
#    responses={404: {"description": "Not found"}},
#)

app.include_router(
    navbar.router,
    prefix="/rapi/v1",
    tags=['navbar'],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    projects.router,
    prefix="/rapi/v1",
    tags=['projects'],
    responses={404: {"description": "Not found"}},
)


logger.info("App started")

#Dev mode
def entry_dev():
    logger.info("Starting app as dev")
    uvicorn.run(app, host="0.0.0.0", port=5000)
    logger.info("App started as dev")

if __name__ == "__main__":
    entry_dev()