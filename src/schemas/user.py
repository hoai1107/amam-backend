from typing import List, Union
from pydantic import BaseModel, Field
import uuid
from datetime import datetime
from .post import Post


class UserBase(BaseModel):
    username: str
    firstname: str
    lastname: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: uuid.UUID
    posts: List[Post] = []

    class Config:
        orm_mode = True
