from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from ..dependencies import get_db, get_current_user

from ..schemas import user
from ..crud import user as user_crud

import uuid

router = APIRouter(
    prefix="/users",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=user.User)
async def create_user(user: user.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    return user_crud.create_user(db, user)


@router.get("/", response_model=List[user.User])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return user_crud.get_users(db, skip=skip, limit=limit)


@router.get("/me", response_model=user.User)
async def get_current_user_info(user: user.User = Depends(get_current_user)):
    return user


@router.get("/{user_id}/follower", response_model=List[user.User])
async def get_follower(user_id: uuid.UUID, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_id(db, user_id)
    return user.followers


@router.get("/{user_id}/followed", response_model=List[user.User])
async def get_followed(user_id: uuid.UUID, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_id(db, user_id)
    return user.followed
