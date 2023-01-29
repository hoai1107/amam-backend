from sqlalchemy.orm import Session, aliased
from sqlalchemy import func

from ..database import models
from ..schemas import comment
import uuid


def create_comment(db: Session, comment: comment.CommentCreate, user_id: uuid.UUID):
    db_comment = models.Comment(**comment.dict(), user_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    return db_comment


def get_comment_by_id(db: Session, comment_id: uuid.UUID):
    db_comment = (
        db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    )

    return db_comment


def delete_comment(db: Session, comment_id: uuid.UUID):
    db_comment = (
        db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    )

    db.delete(db_comment)
    db.commit()
