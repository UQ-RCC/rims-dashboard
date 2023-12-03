from typing import Optional, ForwardRef

from .base_schema import BaseSchema

class WhitelistSchema(BaseSchema):
    email: str
    whitelist: bool