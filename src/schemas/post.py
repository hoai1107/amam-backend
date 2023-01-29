from typing import List, Union
from pydantic import BaseModel, Field
import uuid
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class Post(PostBase):
    id: uuid.UUID
    time_created: datetime = Field(default_factory=datetime.now)
    time_updated: Union[datetime, None] = None
    author_id: uuid.UUID
    number_of_comments: int
    like: int
    dislike: int

    class Config:
        orm_mode = True
