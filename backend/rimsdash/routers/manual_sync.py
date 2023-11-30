import logging

import rimsdash.db as rdb
import rimsdash.collate.processing as processing

logger = logging.getLogger('rimsdash')

def run_sync():
    """
    perform primary sync
    """
    with rdb.sessionmaker.context_session() as db:
        processing.sync_systems(db)    #0 min
        processing.sync_users(db)      #1 min
        processing.sync_projects(db)   #2 min

def run_extended_sync():
    """
    perform extension sync with individual calls
    """
    with rdb.sessionmaker.context_session() as db:
        processing.sync_user_rights(db)    #15 min
        processing.sync_project_users(db)  #5 min
        processing.sync_user_admin(db, skip_existing = True)

def run_state_processing():
    """
    calculate states (local)
    """
    with rdb.sessionmaker.context_session() as db:
        processing.process_projects(db)
        processing.process_users(db) 