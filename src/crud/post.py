from sqlalchemy.orm import Session

from ..schemas import post
from ..database import models
import uuid
import enum


class SortOption(enum.Enum):
    NEWEST = "newest"
    MOST_LIKE = "most_like"
    MOST_COMMENT = "most_comment"


def get_posts(
    db: Session,
    sort_option: SortOption,
    skip: int = 0,
    limit: int = 100,
):
    query = db.query(models.Post)

    if sort_option == SortOption.NEWEST:
        query = query.order_by(models.Post.time_created.desc())
    elif sort_option == SortOption.MOST_LIKE:
        query = query.order_by(models.Post.like.desc())
    elif sort_option == SortOption.MOST_COMMENT:
        query = query.order_by(models.Post.number_of_comments.desc())

    print(query)
    return query.offset(skip).limit(limit).all()


def get_post_by_id(db: Session, post_id: uuid.UUID):
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def update_post(db: Session, post_id: uuid.UUID, post: post.Post, user_id: uuid.UUID):
    db_post = (
        db.query(models.Post)
        .filter(models.Post.id == post_id, models.Post.author_id == user_id)
        .first()
    )
    if db_post is None:
        return None

    for key, value in post.dict().items():
        setattr(db_post, key, value)

    db.commit()
    return db_post


def create_post(db: Session, post: post.PostCreate, user_id: uuid.UUID):
    db_post = models.Post(**post.dict(), author_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


def delete_post(db: Session, post_id: uuid.UUID, user_id: uuid.UUID):
    db_post = (
        db.query(models.Post)
        .filter(models.Post.id == post_id, models.Post.author_id == user_id)
        .first()
    )

    db.delete(db_post)
    db.commit()
    return True
