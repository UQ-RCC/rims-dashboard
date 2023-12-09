import logging

import rimsdash.db as rdb
import rimsdash.config as config
import rimsdash.external.rims as rims
import rimsdash.models as models
import rimsdash.schemas as schemas
import rimsdash.crud as crud

import rimsdash.collate as collate
import rimsdash.routers as routers
import rimsdash.routers.manual_sync as updater

from rimsdash.models import SystemRight, ProjectRight, SyncType


logger = logging.getLogger('rimsdash')

db = rdb.get_session()

#drop and restart
if False:
    rdb.drop_db(force=True)
    rdb.init_db()    

    db = rdb.get_session()


print("STARTING")

if False:
    collate.processing.sync_systems(db)
    print(1)
    collate.processing.sync_users(db)
    print(2)
    project_list = collate.processing.sync_projects(db)
    print(3)

    projectaccount_list.sync_project_accounts(project_list, projectaccount_list, db)
    print(5)    


projectaccount_list = collate.processing.sync_accounts(db)
print(4)
