import logging

import rimsdash.db as rdb
import rimsdash.service.sync as sync

logger = logging.getLogger('rimsdash')

def run_sync():
    """
    perform primary sync
    """
    with rdb.sessionmaker.context_session() as db:
        sync.batch.systems(db)    #0 min
        sync.batch.users(db)      #1 min
        sync.batch.projects(db)   #2 min

def run_extended_sync():
    """
    perform extension sync with individual calls
    """
    with rdb.sessionmaker.context_session() as db:
        sync.batch.user_rights(db)    #15 min
        sync.batch.project_users(db)  #5 min
        sync.sequential.admin_users(db, skip_existing = False)

def run_state_processing():
    """
    calculate states (local)
    """
    with rdb.sessionmaker.context_session() as db:
        sync.processing.process_projects(db)
        sync.processing.process_users(db) 