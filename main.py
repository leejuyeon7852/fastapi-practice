from fastapi import FastAPI
from app.routers import posts
from app.database import Base, engine
from app.models import post

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(posts.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
