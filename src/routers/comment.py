from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse, Response
from ..dependencies import get_current_user, get_db
from sqlalchemy.orm import Session

from ..schemas import user, comment, vote
from ..crud import comment as comment_crud
from ..crud import vote as vote_crud
import uuid
from typing import List

router = APIRouter(
    prefix="/comments",
    tags=["Comment/Reply"],
)


@router.post("/reply", response_model=comment.Comment)
@router.post("/comment", response_model=comment.Comment)
async def create_comment_or_reply(
    comment: comment.CommentCreate,
    db: Session = Depends(get_db),
    user: user.User = Depends(get_current_user),
):
    return comment_crud.create_comment(db, comment, user.id)


@router.get("/{comment_id}", response_model=comment.Comment)
async def get_comment(comment_id: uuid.UUID, db: Session = Depends(get_db)):
    db_comment = comment_crud.get_comment_by_id(db, comment_id)
    db_comment = comment.Comment.from_orm(db_comment)
    return db_comment


@router.delete("/{comment_id}")
async def delete_comment(comment_id: uuid.UUID, db: Session = Depends(get_db)):
    comment_crud.delete_comment(db, comment_id)
    return JSONResponse(
        content="Delete comment successfully.", status_code=status.HTTP_200_OK
    )


@router.get("/reply/{comment_id}", response_model=List[comment.Comment])
async def get_reply_of_comment(comment_id: uuid.UUID, db: Session = Depends(get_db)):
    db_comment = comment_crud.get_comment_by_id(db, comment_id)
    replies = [comment.Comment.from_orm(reply) for reply in db_comment.replies]
    return replies


@router.post("/vote")
async def vote_comment_or_reply(
    vote: vote.CommentVoteCreate,
    user: user.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    vote_crud.vote_comment(db, user.id, **vote.dict())
    return Response(status_code=status.HTTP_200_OK)
