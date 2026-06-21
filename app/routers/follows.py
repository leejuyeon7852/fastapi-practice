from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud import follow as follow_crud
from app.schemas.follow import FollowResponse, FollowUserResponse
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.models.follow import Follow

router = APIRouter()

# 팔로우/언팔로우 토글
@router.post("/users/{user_id}/follow", response_model=FollowResponse)
async def toggle_follow(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return follow_crud.toggle_follow(db, current_user.id, user_id)

# 팔로워 목록 
@router.get("/users/me/followers", response_model=list[FollowUserResponse])
async def get_followers(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return follow_crud.get_followers(db, current_user.id)

# 팔로잉 목록
@router.get("/users/me/following", response_model=list[FollowUserResponse])
async def get_following(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return follow_crud.get_following(db, current_user.id)

# 팔로우 상태 확인
@router.get("/users/{user_id}/follow/status")
async def get_follow_status(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    followed = db.query(Follow).filter(
        Follow.follower_id == current_user.id,
        Follow.following_id == user_id
    ).first() is not None
    return {"followed": followed, "following_id": user_id}
