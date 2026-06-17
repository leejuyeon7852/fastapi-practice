from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import comment as comment_crud
from app.schemas.comment import CommentCreate, CommentResponse
from app.core.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter()

# 댓글 작성
@router.post("/posts/{post_id}/comments", response_model=CommentResponse)
async def create_comment(post_id: int, comment: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return comment_crud.create_comment(db, post_id, current_user.id, comment)

# 대댓글 작성
@router.post("/posts/{post_id}/comments/{comment_id}/replies", response_model=CommentResponse)
async def create_reply(post_id: int, comment_id: int, comment: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return comment_crud.create_comment(db, post_id, current_user.id, comment, parent_id=comment_id)

# 댓글 조회
@router.get("/posts/{post_id}/comments", response_model=list[CommentResponse])
async def get_comments(post_id: int, db: Session = Depends(get_db)):
    return comment_crud.get_comments(db, post_id)

# 댓글/대댓글 삭제
@router.delete("/comments/{comment_id}")
async def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_comment = comment_crud.delete_comment(db, comment_id, current_user.id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다.")
    if db_comment == "forbidden":
        raise HTTPException(status_code=403, detail="본인 댓글만 삭제할 수 있습니다.")
    return {"message": "댓글이 삭제되었습니다."}
