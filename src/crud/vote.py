from ..database import models
from sqlalchemy.orm import Session
import uuid


def vote_post(db: Session, user_id: uuid.UUID, value: int, post_id: uuid.UUID):
    db_post = (
        db.query(models.PostVote)
        .filter(models.PostVote.post_id == post_id, models.PostVote.user_id == user_id)
        .first()
    )

    if db_post is not None:
        if db_post.value == value:
            db.delete(db_post)
        else:
            db_post.value = value
    else:
        db_post = models.PostVote(post_id=post_id, user_id=user_id, value=value)
        db.add(db_post)

    db.commit()


def vote_comment(db: Session, user_id: uuid.UUID, value: int, comment_id: uuid.UUID):
    db_comment = (
        db.query(models.CommentVote)
        .filter(
            models.CommentVote.comment_id == comment_id,
            models.CommentVote.user_id == user_id,
        )
        .first()
    )

    if db_comment is not None:
        if db_comment.value == value:
            db.delete(db_comment)
        else:
            db_comment.value = value
    else:
        db_comment = models.CommentVote(
            comment_id=comment_id, user_id=user_id, value=value
        )
        db.add(db_comment)

    db.commit()
