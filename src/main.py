from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn

from .routers import user, post, auth, comment

load_dotenv()


app = FastAPI()


app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(comment.router)


def start():
    uvicorn.run("src.main:app", reload=True)
