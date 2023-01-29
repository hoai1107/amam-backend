from pydantic import BaseModel, Field
import uuid
from typing import Union, List
from datetime import datetime


class CommentBase(BaseModel):
    content: str
    parent_comment_id: Union[uuid.UUID, None] = None
    post_id: uuid.UUID

    class Config:
        orm_mode = True


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: uuid.UUID
    user_id: uuid.UUID
    time_created: datetime = Field(default_factory=datetime.now)
    number_of_replies: int
    like: int
    dislike: int
