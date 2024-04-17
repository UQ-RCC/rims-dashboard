import logging
import os, sys

import rimsdash.db as rdb
import rimsdash.config as config
import rimsdash.external.rims as rims
import rimsdash.models as models
import rimsdash.schemas as schemas
import rimsdash.crud as crud

import rimsdash.service as service
import rimsdash.routers as routers
import rimsdash.routers.manual_sync as updater

import service.sync as sync
import service.access as access

from logging.handlers import TimedRotatingFileHandler
from rimsdash.models import SystemRight, ProjectRight, SyncType


#--------------------------------------------------------

#logging setup
log_level_in: str = config.get('logging', 'log_level', default = "INFO")

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
#--------------------------------------------------------

db = rdb.get_session()

#drop and restart
if False:
    rdb.drop_db(force=True)
    rdb.init_db()    

    db = rdb.get_session()

syncs = crud.sync.get_latest_completion(db)

#sync.control.run_sync(db, sync_type = SyncType.update)

#if True:        
#    logger.info(">>>>>>>>>>>>Initialising DB")
#    rdb.init_db()
#else:
#    logger.info(">>>>>>>>>>>>DB already initialised")

#logger.info(">>>>>>>>>>>>Sync event triggered")

#with rdb.sessionmaker.context_session() as db:

    #sync.processing.postprocess_projects(db)
    #sync.processing.process_users(db)
    #sync.sequential.admin_users(db)

    #sync.master.calc_states(db)

    #__project = crud.project.get(db, 3151)

    #result = schemas.project_schema.ProjectOutRefsSchema.from_orm(__project)

#    for right in result.user_rights:
#        print(f"{right.user.username}, {right.user.user_state.ok_all}")

print("COMPLETE")


