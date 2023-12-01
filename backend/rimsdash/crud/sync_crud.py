from typing import Optional

from sqlalchemy import desc

from sqlalchemy.orm import Session

from rimsdash.crud.base_crud import CRUDBase
from rimsdash.models.sync_models import SyncModel
from rimsdash.schemas.sync_schema import SyncCreateSchema, SyncCompleteSchema

class CRUDSync(CRUDBase[SyncModel, SyncCreateSchema, SyncCompleteSchema]):
    def get_latest_start(self, db: Session) -> Optional[SyncModel]:
        return db.query(SyncModel).order_by(desc(SyncModel.start_time)).first()

    def get_latest_completion(self, db: Session) -> Optional[SyncModel]:
        return db.query(SyncModel).filter(SyncModel.complete == True).order_by(desc(SyncModel.end_time)).first()

sync = CRUDSync(SyncModel)