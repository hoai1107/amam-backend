import uuid
from enum import IntEnum
from .database import Base

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import TSVECTOR


class TSVector(sa.types.TypeDecorator):
    impl = TSVECTOR


"""
Post model
"""


class Post(Base):
    __tablename__ = "posts"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = sa.Column(sa.Text, nullable=False)
    content = sa.Column(sa.Text, nullable=False)
    time_created = sa.Column(sa.DateTime(timezone=True), server_default=func.now())
    time_updated = sa.Column(sa.DateTime(timezone=True), onupdate=func.now())
    author_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("users.id"))

    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", cascade="all, delete-orphan, delete")
    votes = relationship("PostVote", cascade="all, delete-orphan, delete")

    __ts_vector__ = sa.Column(
        TSVector(),
        sa.Computed("to_tsvector('english', title || ' ' || content)", persisted=True),
    )

    __table_args__ = (
        sa.Index("ix_post__ts_vector__", __ts_vector__, postgresql_using="gin"),
    )

    @hybrid_property
    def like(self):
        return len([vote for vote in self.votes if vote.value == VoteType.LIKE])

    @hybrid_property
    def dislike(self):
        return len([vote for vote in self.votes if vote.value == VoteType.DISLIKE])

    @hybrid_property
    def number_of_comments(self):
        return len(self.comments)

    @like.expression
    def like(cls):
        return (
            sa.select(func.count(PostVote.user_id))
            .where(PostVote.value == VoteType.LIKE, PostVote.post_id == cls.id)
            .label("total_like")
        )

    @dislike.expression
    def dislike(cls):
        return (
            sa.select(func.count(PostVote.user_id))
            .where(PostVote.value == VoteType.DISLIKE, PostVote.post_id == cls.id)
            .label("total_dislike")
        )

    @number_of_comments.expression
    def number_of_comments(cls):
        return (
            sa.select(func.count(Comment.id))
            .where(Comment.post_id == cls.id)
            .label("total_comments")
        )


"""
User model
"""


class User(Base):
    __tablename__ = "users"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = sa.Column(sa.Text, unique=True)
    password = sa.Column(sa.Text, nullable=False)
    firstname = sa.Column(sa.Text, nullable=False)
    lastname = sa.Column(sa.Text, nullable=False)

    posts = relationship("Post", cascade="all, delete", back_populates="author")
    comments = relationship("Comment", cascade="all, delete")


"""
Comment model
"""


class Comment(Base):
    __tablename__ = "comments"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = sa.Column(sa.Text)
    user_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("users.id"))
    post_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("posts.id"))
    time_created = sa.Column(sa.DateTime(timezone=True), server_default=func.now())
    parent_comment_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("comments.id"))

    replies = relationship("Comment", cascade="all, delete", lazy=True)
    votes = relationship("CommentVote", cascade="all, delete-orphan, delete")

    @hybrid_property
    def number_of_replies(self):
        if self.replies:
            return len(self.replies)
        return 0

    # TODO: Need to fix this
    @number_of_replies.expression
    def number_of_replies(cls):
        return (
            sa.select([sa.func.count(Comment.id)])
            .where(Comment.parent_comment_id == cls.id)
            .label("total_reply")
        )

    @hybrid_property
    def like(self):
        return len([vote for vote in self.votes if vote.value == VoteType.LIKE])

    @hybrid_property
    def dislike(self):
        return len([vote for vote in self.votes if vote.value == VoteType.DISLIKE])

    @like.expression
    def like(cls):
        return (
            sa.select(func.count(CommentVote.user_id))
            .where(CommentVote.value == VoteType.LIKE, CommentVote.comment_id == cls.id)
            .label("total_like")
        )

    @dislike.expression
    def dislike(cls):
        return (
            sa.select(func.count(CommentVote.user_id))
            .where(
                CommentVote.value == VoteType.DISLIKE, CommentVote.comment_id == cls.id
            )
            .label("total_dislike")
        )


"""
Vote model (Post & Comment)
"""


class VoteType(IntEnum):
    LIKE: int = 1
    DISLIKE: int = -1


class PostVote(Base):
    __tablename__ = "post_votes"

    post_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("posts.id"), primary_key=True)
    user_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("users.id"), primary_key=True)
    value = sa.Column(sa.INTEGER, nullable=False)

    __table_args__ = (sa.PrimaryKeyConstraint(post_id, user_id),)


class CommentVote(Base):
    __tablename__ = "comment_votes"

    comment_id = sa.Column(
        UUID(as_uuid=True), sa.ForeignKey("comments.id"), primary_key=True
    )
    user_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("users.id"), primary_key=True)
    value = sa.Column(sa.INTEGER, nullable=False)
