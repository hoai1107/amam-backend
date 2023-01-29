from .database.database import SessionLocal
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import uuid
from jose import JWTError, jwt
from sqlalchemy.orm import Session
import os
from .schemas.token import TokenData
from .crud import user as user_crud


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = uuid.UUID(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception

    user = user_crud.get_user_by_id(db, user_id=token_data.user_id)
    if user is None:
        raise credentials_exception

    return user
