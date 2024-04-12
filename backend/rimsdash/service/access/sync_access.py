import logging
import datetime

from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

import rimsdash.db as rdb
import rimsdash.crud as crud

from rimsdash.models import SyncType, SyncStatus
from rimsdash.models.sync_models import SyncModel


logger = logging.getLogger('rimsdash')

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

    def get_last_sync(self, db: Session = Depends(rdb.get_db), match_status: SyncStatus = SyncStatus.complete, accept_minor: bool = True) -> SyncModel:  
        """
        return most recent sync
        """        
        try:
            accepted_types = [ SyncType.full, SyncType.rebuild ]
            last_sync = None

            if accept_minor:
                accepted_types.append(SyncType.update)

            sync_rows = crud.sync.get_sorted_completions(db)

            for sync in sync_rows:
                if sync.status == match_status and sync.sync_type in accepted_types:
                    last_sync = sync
                    break
            
        except Exception as e:
            return None
        
        finally:
            return last_sync    


    def get_sync_delta(self, last_sync: SyncModel) -> datetime.timedelta:
        """
        return timedelta to completion of specified sync
        """          
        try:
            if last_sync is not None:
                delta = datetime.datetime.now() - last_sync.end_time
            else:
                logger.warn(f"no input sync row specified, using nominal delta")
                delta = datetime.timedelta(weeks=52)

        except Exception as e:
            logger.warn(f"invalid sync row specified, using nominal delta")            
            delta = datetime.timedelta(weeks=52)
        
        finally:
            return delta 


    def get_all_recent_syncs(self, db: Session = Depends(rdb.get_db), match_status: SyncStatus = None, \
                             delta: datetime.timedelta = datetime.timedelta(hours=12)) -> list[SyncModel]:  
        """
        return list of sync events by timedelta, with status if specified
        """
        try:

            accepted_types = [ SyncType.update, SyncType.full, SyncType.rebuild ]
            return_list = []

            sync_rows = crud.sync.get_sorted_completions(db)

            for sync in sync_rows:
                if ( match_status == None or sync.status == match_status ) and sync.sync_type in accepted_types:
                    if ( (datetime.datetime.now() - sync.start_time ) <= delta):
                        return_list.append(sync)
                    else:
                        logger.warn(f"found old incomplete sync {sync.id} at time {sync.start_time} with type {sync.sync_type}, status {sync.status}")
            
        except Exception as e:
            return []
        
        finally:
            return return_list

    def get_all_ongoing_syncs(self, db: Session = Depends(rdb.get_db)) -> list[SyncModel]:  
        """
        return most recent sync
        """        
        return_list = self.get_all_recent_syncs(db, match_status = SyncStatus.in_progress)
        
        return return_list        


sync = SyncAccess()