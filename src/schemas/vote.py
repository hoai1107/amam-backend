from pydantic import BaseModel
from ..database.models import VoteType
import uuid


class PostVoteBase(BaseModel):
    post_id: uuid.UUID
    value: VoteType

    class Config:
        orm_mode = True


class PostVoteCreate(PostVoteBase):
    pass


class PostVote(PostVoteBase):
    user_id: uuid.UUID


class CommentVoteBase(BaseModel):
    comment_id: uuid.UUID
    value: VoteType

    class Config:
        orm_mode = True


class CommentVoteCreate(CommentVoteBase):
    pass


class CommentVote(CommentVoteBase):
    user_id: uuid.UUID
