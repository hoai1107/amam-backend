from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn

from .routers import user, post, auth, comment, search

load_dotenv()


app = FastAPI()


@app.get("/")
async def home():
    return "Welcome to AMAM API server"


app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(comment.router)
app.include_router(search.router)


def start():
    uvicorn.run("src.main:app", reload=True)
