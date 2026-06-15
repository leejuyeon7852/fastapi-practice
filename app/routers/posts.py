from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.crud import post as post_crud
from app.schemas.post import PostCreate, PostUpdate, PostResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 게시글 생성
@router.post("/posts", response_model=PostResponse)
async def create_post(post: PostCreate, db: Session = Depends(get_db)):
    return post_crud.create_post(db, post)

# 게시글 전체 조회
@router.get("/posts", response_model=list[PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    return post_crud.get_posts(db)

# 게시글 상세 조회
@router.get("/posts/{post_id}", response_model = PostResponse)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    db_post = post_crud.get_post(db, post_id)

    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return db_post

# 게시글 수정
@router.put("/posts/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, post: PostUpdate, db: Session = Depends(get_db)):
    db_post = post_crud.update_post(db, post_id, post)

    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return db_post

# 게시글 삭제
@router.delete("/posts/{post_id}")
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = post_crud.delete_post(db, post_id)

    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return {"message": "게시글이 삭제 되었습니다."}