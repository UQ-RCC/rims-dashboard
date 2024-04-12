import logging
import datetime

from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

import rimsdash.db as rdb
import rimsdash.crud as crud

from rimsdash.models import SyncType
from rimsdash.models.sync_models import SyncModel

class SyncAccess():
    def __init__(self):    
        pass

    def has_cursor(self, db: Session = Depends(rdb.get_db)) -> bool:
        """
        check for valid db session

        WARNING: called from public endpoint
        """
        try:
            db.execute(text("SELECT 1"))
            return True
        
        except Exception as e:
            return False

    def has_synced(self, db: Session = Depends(rdb.get_db)) -> bool:
        """
        check for completed sync anywhere in db history

        WARNING: called from public endpoint
        """
        try:
            last_sync = crud.sync.get_latest_completion(db)

            if last_sync is not None:
                return True

        except Exception as e:
            return False    

    def get_last_sync(self, db: Session = Depends(rdb.get_db), accept_minor: bool = True) -> SyncModel:  
        """
        return most recent sync
        """        
        try:
            accepted_types = [ SyncType.full ]
            last_sync = None

            if accept_minor:
                accepted_types.append(SyncType.minor)

            sync_rows = crud.sync.get_sorted_completions(db)

            for sync in sync_rows:
                if sync.complete == True and sync.sync_type in accepted_types:
                    last_sync = sync
                    break
            
        except Exception as e:
            return None
        
        finally:
            return last_sync


    def get_last_sync_delta(self, db: Session = Depends(rdb.get_db), accept_minor: bool = True) -> datetime.timedelta:
        """
        return timedelta to completion of most recent sync
        """          
        try:
            last_sync = self.db_last_sync(db, accept_minor = accept_minor)

            if last_sync is not None:
                delta = datetime.datetime.now() - last_sync.end_time
            else:
                delta = datetime.timedelta(weeks=52)

        except Exception as e:
            delta = datetime.timedelta(weeks=52)
        
        finally:
            return delta        




sync = SyncAccess()