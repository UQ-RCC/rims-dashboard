from typing import Optional

from sqlalchemy.orm import Session

from rimsdash.crud.base_crud import CRUDBase
from rimsdash.models.account_models import AccountModel
from rimsdash.schemas.account_schema import AccountReceiveSchema, AccountUpdateSchema

class CRUDAccount(CRUDBase[AccountModel, AccountReceiveSchema, AccountUpdateSchema]):
    ...

account = CRUDAccount(AccountModel)