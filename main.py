from fastapi import FastAPI
from app.routers import posts, users, comments, likes, scraps, follows
from app.database import Base, engine
from app.models import post, user, comment, like, scrap, follow

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(comments.router)
app.include_router(likes.router)
app.include_router(scraps.router)
app.include_router(follows.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
