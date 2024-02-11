import logging
import os 

import rimsdash.db as rdb
import rimsdash.config as config
import rimsdash.external.rims as rims
import rimsdash.models as models
import rimsdash.schemas as schemas
import rimsdash.crud as crud

import rimsdash.service as service
import rimsdash.routers as routers
import rimsdash.routers.manual_sync as updater

from logging.handlers import TimedRotatingFileHandler
from rimsdash.models import SystemRight, ProjectRight, SyncType


#--------------------------------------------------------
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
logging.getLogger("uvicorn").addHandler(fh)
#--------------------------------------------------------

db = rdb.get_session()

#drop and restart
if False:
    rdb.drop_db(force=True)
    rdb.init_db()    

    db = rdb.get_session()


print("STARTING")
#service.processing.postprocess_projects(db)
service.processing.sync_projects(db)
print("U done")


