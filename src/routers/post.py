from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse, Response
from typing import List
from sqlalchemy.orm import Session
import uuid
from ..dependencies import get_db, get_current_user

from ..schemas import post, user, comment, vote
from ..crud import post as post_crud
from ..crud import vote as vote_crud

router = APIRouter(
    prefix="/posts",
    tags=["Post"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=post.Post)
async def create_post(
    post: post.PostCreate,
    db: Session = Depends(get_db),
    user: user.User = Depends(get_current_user),
):
    db_post = post_crud.create_post(db, post, user.id)
    return db_post


@router.get("/", response_model=List[post.Post])
async def get_all_posts(
    sort_option: post_crud.SortOption = post_crud.SortOption.NEWEST,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return post_crud.get_posts(db, skip=skip, limit=limit, sort_option=sort_option)


@router.get("/{post_id}", response_model=post.Post)
async def get_single_post(post_id: uuid.UUID, db: Session = Depends(get_db)):
    db_post = post_crud.get_post_by_id(db, post_id)
    if db_post == None:
        raise HTTPException(status_code=404, detail="Post ID not found.")
    return db_post


@router.get("/{post_id}/comments", response_model=List[comment.Comment])
async def get_post_comments(post_id: uuid.UUID, db: Session = Depends(get_db)):
    post = post_crud.get_post_by_id(db, post_id)
    if post == None:
        raise HTTPException(status_code=404, detail="Post ID not found.")

    comments = [
        comment.Comment.from_orm(cmt)
        for cmt in post.comments
        if cmt.parent_comment_id is None
    ]

    return comments


@router.put("/{post_id}", response_model=post.Post)
async def update_post(
    post_id: uuid.UUID,
    post_content: post.PostUpdate,
    db: Session = Depends(get_db),
    user: user.User = Depends(get_current_user),
):
    updated_post = post_crud.update_post(db, post_id, post_content, user.id)
    if updated_post is None:
        raise HTTPException(status_code=404, detail="Post not found.")

    return updated_post


@router.delete("/{post_id}")
async def delete_post(
    post_id: uuid.UUID,
    user: user.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    row_count = post_crud.delete_post(db, post_id, user.id)
    if not row_count:
        return JSONResponse(
            content="Post not found.", status_code=status.HTTP_404_NOT_FOUND
        )

    return JSONResponse(content="Delete post successfully.")


@router.post("/vote")
async def vote_post(
    vote: vote.PostVoteCreate,
    user: user.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    vote_crud.vote_post(db, user.id, **vote.dict())
    return Response(status_code=status.HTTP_200_OK)
