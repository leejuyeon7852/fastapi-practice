from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud import like as like_crud
from app.schemas.like import LikeResponse
from app.core.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter()

# 게시글 좋아요 토글
@router.post("/posts/{post_id}/like", response_model=LikeResponse)
async def toggle_post_like(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return like_crud.toggle_like(db, current_user.id, current_user.nickname, post_id=post_id)

# 댓글 좋아요 토글
@router.post("/comments/{comment_id}/like", response_model=LikeResponse)
async def toggle_comment_like(comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return like_crud.toggle_like(db, current_user.id, current_user.nickname, comment_id=comment_id)
