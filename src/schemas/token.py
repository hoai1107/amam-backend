from pydantic import BaseModel
from typing import Union
import uuid


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Union[uuid.UUID, None] = None
