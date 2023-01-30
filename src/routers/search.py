from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas import post
from ..crud import post as post_crud
from ..dependencies import get_db

from typing import List

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/posts", response_model=List[post.Post])
async def search_posts(
    search_term: str,
    skip: int = 0,
    limit: int = 100,
    sort_option: post_crud.SortOption = post_crud.SortOption.NEWEST,
    db: Session = Depends(get_db),
):
    return post_crud.get_posts(
        db, search_term=search_term, sort_option=sort_option, skip=skip, limit=limit
    )
