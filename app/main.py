from fastapi import FastAPI

from app.memes.router import router as meme_router
from app.users.router import router as user_router

app = FastAPI()

app.include_router(user_router, prefix='/api/v1')
app.include_router(meme_router, prefix='/api/v1')